from app.services.satellite_query_service import get_all_satellites
from app.collision.detector import group_satellites_by_band

satellites = get_all_satellites()
bands = group_satellites_by_band(satellites)

print("Number of bands used:", len(bands))
for band, sats in list(bands.items())[:5]:
    print(f"Band {band}: {len(sats)} satellites")