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