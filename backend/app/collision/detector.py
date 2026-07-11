from itertools import combinations
from app.orbit.propagator import estimate_altitude_km, get_altitude_band
from app.database.database import SessionLocal
from app.database.models import CloseApproachDB
from app.collision.distance import find_closest_approach
from skyfield.api import load


def scan_for_close_approaches(satellites: list, hours: int = 6, step_minutes: int = 5,
                               threshold_km: float = 100, band_width_km: float = 50):
    """
    here i created this functon to check every unique pair within the same altitude band for close
    approaches within the next `hours`. Saves any result under
    `threshold_km` to the database.
    """
    db = SessionLocal()
    bands = group_satellites_by_band(satellites, band_width_km)

    for band, sats_in_band in bands.items():
        print(f"Scanning band {band}: {len(sats_in_band)} satellites, {len(sats_in_band) * (len(sats_in_band) - 1) // 2} pairs")
        for sat1, sat2 in combinations(sats_in_band, 2):
            result = find_closest_approach(sat1, sat2, hours, step_minutes)

            if result["min_distance_km"] < threshold_km:
                approach = CloseApproachDB(
                    satellite_1_norad_id=sat1.norad_id,
                    satellite_2_norad_id=sat2.norad_id,
                    min_distance_km=result["min_distance_km"],
                    closest_time_utc=result["time"].utc_iso(),
                )
                db.add(approach)

    db.commit()
    db.close()

def group_satellites_by_band(satellites: list, band_width_km: float = 50) -> dict:
    """
    creted this function for grouping satellites into a dict keyed by altitude band.
    
    """
    bands = {}

    for sat in satellites:
        altitude = estimate_altitude_km(sat)
        band = get_altitude_band(altitude, band_width_km)

        bands.setdefault(band, []).append(sat)

    return bands