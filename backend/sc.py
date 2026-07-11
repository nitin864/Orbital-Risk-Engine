from app.services.satellite_query_service import get_all_satellites
from app.collision.detector import scan_for_close_approaches
import time

satellites = get_all_satellites()

start = time.time()
scan_for_close_approaches(
    satellites,
    hours=2,
    step_minutes=15,
    threshold_km=5000,
    altitude_band_width_km=50,
    inclination_band_width_deg=1,
)
elapsed = time.time() - start

print(f"Scan complete in {elapsed:.1f} seconds")