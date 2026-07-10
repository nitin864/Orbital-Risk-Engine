from skyfield.api import load, EarthSatellite, wgs84

from app.models.satellite import Satellite

_ts = load.timescale()


def get_current_position(satellite: Satellite):
    """
    Takes our own Satellite model (with line1, line2, name)
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
    