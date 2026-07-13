import re


def parse_international_designator(line1: str) -> str | None:
    """
   created this function to  Extracts the COSPAR international designator from a TLE line 1, 

     
    """
    if not line1 or len(line1) < 17:
        return None

    raw = line1[9:17].strip()
    match = re.match(r"^(\d{2})(\d{3})([A-Za-z]*)$", raw)
    if not match:
        return None

    yy, launch_num, piece = match.groups()
    year = int(yy)
    full_year = 1900 + year if year >= 57 else 2000 + year
    return f"{full_year}-{launch_num}{piece}"


def classify_orbit_shape(eccentricity: float) -> str:
    """Rough circular-vs-elliptical bucket from eccentricity."""
    if eccentricity is None:
        return "UNKNOWN"
    return "CIRCULAR" if eccentricity < 0.01 else "ELLIPTICAL"


 
_CONSTELLATION_PREFIXES = {
    "STARLINK": "Starlink",
    "ONEWEB": "OneWeb",
    "IRIDIUM": "Iridium",
    "GPS": "GPS",
    "GLONASS": "GLONASS",
    "GALILEO": "Galileo",
    "BEIDOU": "BeiDou",
    "COSMOS": "Cosmos",
    "ISS": "ISS",
    "NOAA": "NOAA",
    "GOES": "GOES",
    "INTELSAT": "Intelsat",
    "SES": "SES",
}


def guess_constellation(name: str) -> str | None:
    if not name:
        return None
    upper = name.upper()
    for prefix, label in _CONSTELLATION_PREFIXES.items():
        if upper.startswith(prefix):
            return label
    return None