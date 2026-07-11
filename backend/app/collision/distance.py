from skyfield.api import load
from app.models.satellite import Satellite
from app.orbit.propagator import get_xyz_at_time


def calculate_distance_km(pos1: tuple, pos2: tuple) -> float:
    """
    in this function taking x,y,z coordinates and calculating the straight-line 
    Eucidean in km
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    distance = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
    return distance ** 0.5

def find_closest_approach(sat1: Satellite, sat2: Satellite, hours: int, step_minutes: int):
    """
    in this function, checking the distance between two satellites at regular time steps
    over the next hours, and returns the minimum distance found
    and when it occurred.
    """
    ts = load.timescale()
    t = ts.now()
    total_minutes = 60 * hours
    steps = total_minutes // step_minutes

    min_distance = None
    min_time = None

    for i in range(steps):
        current_time = t + (i * step_minutes / 1440)
        pos1 = get_xyz_at_time(sat1, current_time)["position"]
        pos2 = get_xyz_at_time(sat2, current_time)["position"]
        distance = calculate_distance_km(pos1, pos2)

        if min_distance is None or distance < min_distance:
            min_distance = distance
            min_time = current_time

    return {"min_distance_km": min_distance, "time": min_time}

def calculate_relative_velocity(vel1: tuple, vel2: tuple) -> float:
    """
    creating this function to calculate the relative speed (km/s) between two velocity vectors.
    """
    vx1, vy1, vz1 = vel1
    vx2, vy2, vz2 = vel2
    velocity_squared = (vx2 - vx1) ** 2 + (vy2 - vy1) ** 2 + (vz2 - vz1) ** 2
    return velocity_squared ** 0.5