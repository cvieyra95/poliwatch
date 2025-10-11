from __future__ import annotations
import os, httpx
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY  = os.getenv("CONGRESS_API_KEY", "")
BASE_URL = os.getenv("CONGRESS_BASE_URL", "https://api.congress.gov/v3/member")
PAGE_SIZE = int(os.getenv("CONGRESS_PAGE_SIZE", "250"))

class CongressClient:
    def __init__(self, api_key: str = API_KEY):
        if not api_key:
            raise RuntimeError("CONGRESS_API_KEY missing")
        self.client = httpx.Client(timeout=30)
        self.api_key = api_key

    def get_member_detail(self, bioguide_id: str) -> dict:
        url = f"{BASE_URL}/{bioguide_id}"
        r = self.client.get(url, params={"api_key": self.api_key, "format": "json"})
        r.raise_for_status()
        return r.json()

    def get_members_page(self, offset: int = 0, page_size: int = PAGE_SIZE) -> tuple[list[dict], int | None]:
            """Returns (items, next_offset or None)."""
            params = {
                "api_key": self.api_key,
                "format": "json",
                "offset": offset,
                "limit": page_size,          # some deployments call this pageSize/limit; keep both
                "pageSize": page_size,
            }
            r = self.client.get(BASE_URL, params=params)
            r.raise_for_status()
            data = r.json()

            items = data.get("members") or data.get("results") or data.get("data") or []
            # very forgiving pagination
            pag   = data.get("pagination") or {}
            if pag.get("next") is not None:
                next_offset = offset + page_size
            elif len(items) < page_size:
                next_offset = None
            else:
                next_offset = offset + page_size
            return items, next_offset

    def close(self):
        self.client.close()
