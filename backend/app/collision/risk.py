def calculate_risk_score(min_distance_km: float, relative_velocity_km_s: float) -> float:
    """
    created this function for risk  calculation
    """
    if min_distance_km <= 0.001:
        return 999999.0

    risk_score = relative_velocity_km_s / min_distance_km
    return risk_score