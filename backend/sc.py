from app.models.satellite import Satellite
from app.collision.distance import find_closest_approach

sat1 = Satellite(
    name="CALSPHERE 1",
    line1="1 00900U 64063C   26189.91071529  .00000426  00000+0  42409-3 0  9991",
    line2="2 00900  90.2218  72.2807 0023416 224.7453 253.6264 13.76645956 74418",
    norad_id="00900",
    inclination=90.2218,
    eccentricity=0.0023416,
    mean_motion=13.76645956,
    orbital_period_minutes=104.6
)

sat2 = Satellite(
    name="CALSPHERE 2",
    line1="1 00902U 64063E   26189.99802150  .00000023  00000+0  20893-4 0  9990",
    line2="2 00902  90.2354  76.3174 0019161 158.2203 267.4625 13.52902150859218",
    norad_id="00902",
    inclination=90.2354,
    eccentricity=0.0019161,
    mean_motion=13.52902150859218,
    orbital_period_minutes=105.7
)

result = find_closest_approach(sat1, sat2, hours=2, step_minutes=15)
print(result)