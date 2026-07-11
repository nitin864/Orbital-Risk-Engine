from app.models.satellite import Satellite
from app.orbit.propagator import get_xyz_and_velocity_at_time
from skyfield.api import load


my_sat = Satellite(
    name="CALSPHERE 2",
    line1="1 00902U 64063E   26189.99802150  .00000023  00000+0  20893-4 0  9990",
    line2="2 00902  90.2354  76.3174 0019161 158.2203 267.4625 13.52902150859218",
    norad_id="00902",
    inclination=90.2354,
    eccentricity=0.0019161,
    mean_motion=13.52902150859218,
    orbital_period_minutes=105.7
)

ts = load.timescale()
now = ts.now()

result = get_xyz_and_velocity_at_time(my_sat, now)
print(result)