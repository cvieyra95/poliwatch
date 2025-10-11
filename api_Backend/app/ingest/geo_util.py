from enums import Chamber

STATE_CODES = {
    "ALABAMA":"AL",
    "ALASKA":"AK",
    "ARIZONA":"AZ",
    "ARKANSAS":"AR",
    "CALIFORNIA":"CA",
    "COLORADO":"CO",
    "CONNECTICUT":"CT",
    "DELAWARE":"DE",
    "FLORIDA":"FL",
    "GEORGIA":"GA",
    "HAWAII":"HI",
    "IDAHO":"ID",
    "ILLINOIS":"IL",
    "INDIANA":"IN",
    "IOWA":"IA",
    "KANSAS":"KS",
    "KENTUCKY":"KY",
    "LOUISIANA":"LA",
    "MAINE":"ME",
    "MARYLAND":"MD",
    "MASSACHUSETTS":"MA",
    "MICHIGAN":"MI",
    "MINNESOTA":"MN",
    "MISSISSIPPI":"MS",
    "MISSOURI":"MO",
    "MONTANA":"MT",
    "NEBRASKA":"NE",
    "NEVADA":"NV",
    "NEW HAMPSHIRE":"NH",
    "NEW JERSEY":"NJ",
    "NEW MEXICO":"NM",
    "NEW YORK":"NY",
    "NORTH CAROLINA":"NC",
    "NORTH DAKOTA":"ND",
    "OHIO":"OH",
    "OKLAHOMA":"OK",
    "OREGON":"OR",
    "PENNSYLVANIA":"PA",
    "RHODE ISLAND":"RI",
    "SOUTH CAROLINA":"SC",
    "SOUTH DAKOTA":"SD",
    "TENNESSEE":"TN",
    "TEXAS":"TX",
    "UTAH":"UT",
    "VERMONT":"VT",
    "VIRGINIA":"VA",
    "WASHINGTON":"WA",
    "WEST VIRGINIA":"WV",
    "WISCONSIN":"WI",
    "WYOMING":"WY",
    # territories / DC
    "DISTRICT OF COLUMBIA":"DC",
    "PUERTO RICO":"PR",
    "GUAM":"GU",
    "VIRGIN ISLANDS":"VI",
    "AMERICAN SAMOA":"AS",
    "NORTHERN MARIANA ISLANDS":"MP",
}

def _state_code(v: str | None) -> str | None:
    if not v:
        return None                    
    v = v.strip()
    if len(v) == 2 and v.isalpha():
        return v.upper()               
    return STATE_CODES.get(v.upper())  

def _norm_district(raw: object, chamber: "Chamber") -> int | None:
    if chamber == Chamber.Senate:
        return None
    if raw in (None, "", "AL", "At Large", "AT-LARGE"):  # common strings
        return 0
    try:
        district = int(raw)
    except Exception:
        return 0
    if district in (98, 99):   # Congress.gov sentinel values
        return 0
    return district
