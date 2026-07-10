# OrbitShield — Progress Log

## Status: Chapter 8 — collision detection

### Done
- Chapter 2: TLE download + caching from CelesTrak (app/services/tle_downloader.py)
- Chapter 3: Parse TLE into Satellite model, extract norad_id, inclination,
  eccentricity, mean_motion, orbital_period_minutes
- Chapter 5: Skyfield orbit propagation
  - app/orbit/propagator.py
  - get_current_position(satellite) -> current lat/lon/altitude
  - get_position_at_time(satellite, time) -> position at arbitrary time
  - Both tested and working
-Module 6 — Coordinate Systems (Raw XYZ for Distance Math)

