## Module 8 — Collision Detection Algorithm
Status: 🔶 Partial (~60%)

### Done
- Distance function (Euclidean, app/collision/distance.py)
- find_closest_approach() — min distance over time window, per pair
- Pairwise brute-force scan (app/collision/detector.py, scan_for_close_approaches)
- Persistence — close_approaches table, working
- Tested at small scale: 20 satellites, 190 pairs, 55 flagged (threshold=5000km)
- API endpoint: GET /conjunctions — working

### In progress / next up
- Altitude pre-filter to make full-scale (15,985 satellites) scanning feasible
  - File: app/orbit/propagator.py (or new file)
  - Function to write: estimate_altitude_km(satellite) -> float
  - Formula (Kepler's third law, no SGP4 needed):
    n (rad/s) = mean_motion * 2π / 86400
    a (semi-major axis, km) = (MU / n**2) ** (1/3), MU = 398600.4418
    altitude ≈ a - 6378.137 (Earth radius km)
  - Sanity check target: CALSPHERE 1 (mean_motion=13.76645956) should
    give altitude ≈ 990-1000 km (matches known Skyfield-measured value)
  - Was mid-implementation when paused — scaffold given, not yet written

### Not started
- Altitude-band bucketing logic
- Only running full pairwise check within same/adjacent bands
- Realistic threshold_km (currently tested loose at 5000km, real value should be single-digit km)
- Running scan against full 15,985-satellite dataset