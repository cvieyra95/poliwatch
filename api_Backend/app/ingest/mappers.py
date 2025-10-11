from __future__ import annotations
from typing import Optional
from dateutil.parser import isoparse
from datetime import datetime, timezone   # CHANGED: keep a single import of timezone
from enums import Party, Chamber
from app.ingest.geo_util import _state_code, _norm_district
from typing import Any, Iterable, List, Optional

def _parse_dt(v: Optional[str]) -> Optional[datetime]:
    if not v:
        return None
    try:
        dt = isoparse(v)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _party(s: Optional[str]) -> Optional[Party]:
    if not s:
        return None
    s = s.strip().lower()
    if s.startswith("dem"):
        return Party.Democratic
    if s.startswith("rep"):
        return Party.Republican
    if s.startswith("ind"):
        return Party.Independent
    if s.startswith("lib"):
        return Party.Libertarian
    return Party.Other


def _chamber(s: Optional[str]) -> Chamber:
    return Chamber.Senate if (s or "").lower().startswith("sen") else Chamber.House


def _split_name_str(s: str) -> tuple[str, str, str | None]:
    s = (s or "").strip()
    if "," in s:  # "Last, First Middle"
        last, rest = [p.strip() for p in s.split(",", 1)]
        parts = rest.split()
        first = parts[0] if parts else ""
        middle = " ".join(parts[1:]) or None
    else:        # "First Middle Last"
        parts = s.split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""
        middle = " ".join(parts[1:-1]) or None
    return first, last, middle


def normalize_member(item: dict) -> dict:
    name = item.get("name")

    if isinstance(name, dict):
        first = item.get("firstName") or name.get("first") or item.get("first_name") or ""
        middle = item.get("middleName") or name.get("middle") or None
        last = item.get("lastName") or name.get("last") or item.get("last_name") or ""
        display_name = (
            item.get("officialName") or item.get("displayName")
            or name.get("officialFull") or f"{first} {last}".strip()
        )
    elif isinstance(name, str):
        first, last, middle = _split_name_str(name)
        display_name = item.get("officialName") or item.get("displayName") or name
    else:
        first = item.get("firstName") or item.get("first_name") or ""
        middle = item.get("middleName") or None
        last = item.get("lastName") or item.get("last_name") or ""
        display_name = item.get("officialName") or item.get("displayName") or f"{first} {last}".strip()

    bioguide_id = (item.get("bioguideId") or item.get("bioguide_id") or "").strip()
    party = _party(item.get("partyName") or item.get("party"))
    chamber = _chamber(item.get("chamber") or item.get("chamberName"))
    state = _state_code(  # CHANGED: remove accidental double assignment
        item.get("stateCode") or item.get("state") or item.get("stateAbbreviation")
    )
    district = _norm_district(item.get("district"), chamber)

    img_url = (item.get("depiction") or {}).get("imageUrl") or item.get("img_url") or None
    profile_url = item.get("url") or item.get("profile_url") or None
    in_office = bool(  # CHANGED: remove accidental double assignment
        str(item.get("inOffice", item.get("in_office", True))).strip().lower() in ("true", "1", "yes", "y", "t")
    )

    return {
        "bioguide_id": bioguide_id,
        "first_name": first,
        "middle_name": middle,
        "last_name": last,
        "display_name": display_name,
        "img_url": img_url,
        "profile_url": profile_url,
        "in_office": in_office,
        "party": party,
        "state": state,
        "district": district,
        "chamber": chamber,
        "created_at": None,
        "updated_at": None,
        "source_updated_at": None,
    }

def _iter_nodes(obj: Any) -> Iterable[Any]:
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _iter_nodes(v)
    elif isinstance(obj, list):
        for x in obj:
            yield from _iter_nodes(x)

def _looks_like_term(d: Any) -> bool:
    if not isinstance(d, dict):
        return False
    has_state   = any(k in d for k in ("state","stateCode","stateAbbreviation"))
    has_chamber = any(k in d for k in ("chamber","chamberName","type"))
    # ADD startYear/start_year so year-only terms are picked up in weird payloads
    has_start   = any(k in d for k in ("startYear","start_year","start_date","startDate","start","begin"))
    return has_state and has_chamber and has_start


def _unwrap_list(x: Any) -> List[dict]:
    if isinstance(x, list):
        return [t for t in x if isinstance(t, dict)]
    if isinstance(x, dict):
        for key in ("items","item","term","terms","data","list"):
            v = x.get(key)
            if isinstance(v, list):
                return [t for t in v if isinstance(t, dict)]
    return []

def _to_int(x) -> Optional[int]:
    try:
        return int(x)
    except Exception:
        return None

def normalize_terms(item: dict) -> list[dict]:
    root = item.get("member", item)

    # Unwrap the terms block from various shapes
    raw_terms = root.get("terms") or root.get("memberTerms") or root.get("roles") or {}
    terms_list = _unwrap_list(raw_terms)
    if not terms_list:
        terms_list = [d for d in _iter_nodes(root) if _looks_like_term(d)]

    out: list[dict] = []
    for t in terms_list:
        ch = _chamber(t.get("chamber") or t.get("chamberName") or t.get("type"))
        st = _state_code(t.get("stateCode") or t.get("state") or t.get("stateAbbreviation"))
        district = _norm_district(t.get("district") or t.get("districtNumber") or t.get("cd"), ch)
        party = _party(t.get("party") or t.get("partyName") or t.get("partyAffiliation"))

        # CHANGED: pull congress + year ints instead of parsing datetimes
        congress   = _to_int(t.get("congress") or t.get("congressNumber") or t.get("session"))
        start_year = _to_int(t.get("startYear") or t.get("start_year"))
        end_year   = _to_int(t.get("endYear")   or t.get("end_year"))

        # Require minimum viable row
        if not (congress and ch and st and start_year):
            continue

        out.append({
            "congress": congress,     # NEW
            "chamber": ch,
            "state": st,
            "district": district,
            "party": party,
            "start_year": start_year, # NEW
            "end_year": end_year,     # NEW (None if ongoing)
        })
    return out

