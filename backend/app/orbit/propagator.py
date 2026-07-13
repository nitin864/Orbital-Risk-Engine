from skyfield.api import load, EarthSatellite, wgs84
import math
from app.models.satellite import Satellite
 

_ts = load.timescale()


def get_current_position(satellite: Satellite):
    """
    taking our own Satellite model (with line1, line2, name)
    and returns its current latitude, longitude, and altitude.
    """
    sky_satellite = EarthSatellite(satellite.line1, satellite.line2, satellite.name)

    t = _ts.now()
    geocentric = sky_satellite.at(t)
    subpoint = wgs84.subpoint(geocentric)

    return {
        "latitude": float(subpoint.latitude.degrees),
        "longitude": float(subpoint.longitude.degrees),
        "altitude_km": float(subpoint.elevation.km),
    }
    
def get_position_at_time(satellite: Satellite, time):
    """
    Returns the satellite's position at a specific time
    (instead of "now").
    """
    sky_satellite = EarthSatellite(satellite.line1, satellite.line2, satellite.name)

    geocentric = sky_satellite.at(time)
    subpoint = wgs84.subpoint(geocentric)

    return {
        "latitude": float(subpoint.latitude.degrees),
        "longitude": float(subpoint.longitude.degrees),
        "altitude_km": float(subpoint.elevation.km),
    }
    
def get_xyz_at_time(satellite: Satellite, time):
    """
    returns the raw (x, y, z) position in km, relative to Earth's center.
    """
    sky_satellite = EarthSatellite(satellite.line1, satellite.line2, satellite.name)
    geocentric = sky_satellite.at(time)
    x,y,z = geocentric.position.km
    
    return {
        "position": (float(x), float(y), float(z)),
    }

def estimate_altitude_km(satellite: Satellite) -> float:
    """
    estimating orbital altitude from mean_motion using Kepler's third law.
    Much cheaper than full SGP4 propagation — used for pre-filtering
    satellite pairs before expensive collision checks.
    """
    MU = 398600.4418  
    EARTH_RADIUS_KM = 6378.137

     
    n = satellite.mean_motion * 2*math.pi/86400
   
    a = (MU / n**2) ** (1/3)
    
   
    return a-EARTH_RADIUS_KM 

def get_altitude_band(altitude_km: float, band_width_km: float = 50) -> int:
    """
    created this function to returns which altitude band a given altitude falls into.
    E.g. with band_width_km=50: 992 km -> band 19 (950-1000 km range)
    """
    return int(altitude_km // band_width_km)


def get_inclination_band(inclination_deg: float, band_width_deg: float = 1) -> int:
    """
    Returns which inclination band a given inclination falls into.
    """
    return int(inclination_deg // band_width_deg)

def get_xyz_and_velocity_at_time(satellite: Satellite, time):
    """
    created this function to return both position (x, y, z in km) and velocity (vx, vy, vz in km/s)
    at a specific time. Velocity is needed for relative-velocity risk scoring.
    """
    sky_satellite = EarthSatellite(satellite.line1, satellite.line2, satellite.name)
    geocentric = sky_satellite.at(time)

    x, y, z = geocentric.position.km
    vx, vy, vz = geocentric.velocity.km_per_s

    return {
        "position": (float(x), float(y), float(z)),
        "velocity": (float(vx), float(vy), float(vz)),
    }


def get_next_pass(satellite: Satellite, lat: float, lon: float, hours: int = 48, min_elevation_deg: float = 10.0):
    """
    Finds the next time this satellite rises above `min_elevation_deg` as
    seen from the given lat/lon. Uses Skyfield's find_events, which does a
    proper topocentric rise/culminate/set calculation (accounts for Earth's
    rotation and the observer's local horizon) rather than a rough
    subpoint-distance approximation.

    Returns None if no pass starts within the search window.
    """
    sky_satellite = EarthSatellite(satellite.line1, satellite.line2, satellite.name)
    observer = wgs84.latlon(lat, lon)

    t0 = _ts.now()
    t1 = _ts.tt_jd(t0.tt + hours / 24)

    times, events = sky_satellite.find_events(observer, t0, t1, altitude_degrees=min_elevation_deg)

    rise_time = None
    culminate_time = None
    set_time = None
    for ti, event in zip(times, events):
        if event == 0:  
            rise_time = ti
            culminate_time = None
            set_time = None
        elif event == 1:  
            culminate_time = ti
        elif event == 2:  # set
            set_time = ti
            if rise_time is not None:
                break   

    if rise_time is None:
        return None

    now_dt = t0.utc_datetime()
    rise_dt = rise_time.utc_datetime()
    minutes_until_rise = (rise_dt - now_dt).total_seconds() / 60

    return {
        "rise_utc": rise_dt.isoformat(),
        "culminate_utc": culminate_time.utc_datetime().isoformat() if culminate_time is not None else None,
        "set_utc": set_time.utc_datetime().isoformat() if set_time is not None else None,
        "minutes_until_rise": minutes_until_rise,
    }