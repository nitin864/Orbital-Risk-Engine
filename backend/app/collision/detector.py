from itertools import combinations

from skyfield.api import load

from app.orbit.propagator import estimate_altitude_km, get_altitude_band, get_inclination_band
from app.database.database import SessionLocal
from app.database.models import CloseApproachDB
from app.collision.distance import find_closest_approach
from app.collision.risk import calculate_risk_score


def group_satellites_by_band(satellites: list, altitude_band_width_km: float = 50,
                              inclination_band_width_deg: float = 5) -> dict:
    """
    Groups satellites into a dict keyed by (altitude_band, inclination_band).
    """
    bands = {}

    for sat in satellites:
        altitude = estimate_altitude_km(sat)
        alt_band = get_altitude_band(altitude, altitude_band_width_km)
        incl_band = get_inclination_band(sat.inclination, inclination_band_width_deg)

        key = (alt_band, incl_band)
        bands.setdefault(key, []).append(sat)

    return bands


def get_neighboring_satellites(bands: dict, band_key: tuple) -> list:
    """
    Given a band key (alt_band, incl_band), returns all satellites
    in that band PLUS satellites in the 8 neighboring bands
    (one step in each direction, both dimensions).
    Not currently used by scan_for_close_approaches (which does its
    own neighbor expansion with a wider +/-2 radius), kept for reference.
    """
    alt_band, incl_band = band_key
    neighbors = []

    for alt_offset in [-1, 0, 1]:
        for incl_offset in [-1, 0, 1]:
            neighbor_key = (alt_band + alt_offset, incl_band + incl_offset)
            if neighbor_key in bands:
                neighbors.extend(bands[neighbor_key])

    return neighbors


def _check_and_save_pair(db, sat1, sat2, hours, step_minutes, threshold_km):
    result = find_closest_approach(sat1, sat2, hours, step_minutes)

    if 0.5 < result["min_distance_km"] < threshold_km:
        risk_score = calculate_risk_score(result["min_distance_km"], result["relative_velocity_km_s"])

        approach = CloseApproachDB(
            satellite_1_norad_id=sat1.norad_id,
            satellite_2_norad_id=sat2.norad_id,
            min_distance_km=result["min_distance_km"],
            closest_time_utc=result["time"].utc_iso(),
            risk_score=risk_score,
        )
        db.add(approach)


def scan_for_close_approaches(satellites: list, hours: int = 6, step_minutes: int = 5,
                               threshold_km: float = 100, altitude_band_width_km: float = 50,
                               inclination_band_width_deg: float = 5):
    """
    Checks satellite pairs within the same or nearby (+/-2) altitude/inclination
    bands for close approaches within the next `hours`. Saves any result under
    `threshold_km` to the database.
    """
    db = SessionLocal()
    bands = group_satellites_by_band(satellites, altitude_band_width_km, inclination_band_width_deg)

    for band_key, sats_in_band in bands.items():
        print(f"Band {band_key}: {len(sats_in_band)} satellites")

       
        for sat1, sat2 in combinations(sats_in_band, 2):
            _check_and_save_pair(db, sat1, sat2, hours, step_minutes, threshold_km)

        
        alt_band, incl_band = band_key
        for alt_offset in [-2, -1, 0, 1, 2]:
            for incl_offset in [-2, -1, 0, 1, 2]:
                if alt_offset == 0 and incl_offset == 0:
                    continue

                neighbor_key = (alt_band + alt_offset, incl_band + incl_offset)

                if neighbor_key <= band_key:
                    continue

                if neighbor_key in bands:
                    for sat1 in sats_in_band:
                        for sat2 in bands[neighbor_key]:
                            _check_and_save_pair(db, sat1, sat2, hours, step_minutes, threshold_km)

    db.commit()
    db.close()