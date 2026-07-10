from skyfield.api import load


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
    over the next `hours`, and returns the minimum distance found
    and when it occurred.
    """
    