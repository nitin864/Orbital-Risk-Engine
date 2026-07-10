def calculate_distance_km(pos1: tuple, pos2: tuple) -> float:
    """
    in this function taking x,y,z coordinates and calculating the straight-line 
    Eucidean in km
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    distance = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
    return distance ** 0.5