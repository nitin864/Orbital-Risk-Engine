from app.models.satellite import Satellite
from app.orbit.propagator import get_current_position

my_sat = Satellite(
    name="CALSPHERE 1",
    line1="1 00900U 64063C   26189.91071529  .00000426  00000+0  42409-3 0  9991",
    line2="2 00900  90.2218  72.2807 0023416 224.7453 253.6264 13.76645956 74418",
    norad_id="00900",
    inclination=90.2218,
    eccentricity=0.0023416,
    mean_motion=13.76645956,
    orbital_period_minutes=104.6
)

print(get_current_position(my_sat))