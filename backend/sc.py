from app.services.satellite_query_service import get_all_close_approaches

results = get_all_close_approaches()
print("Count:", len(results))
print(results[0].satellite_1_norad_id, results[0].min_distance_km)