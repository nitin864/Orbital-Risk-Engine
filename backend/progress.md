# OrbitShield — Progress Log

## Status: Chapter 5 — Orbit Propagation (Skyfield)

### Done
- Chapter 2: TLE download + caching from CelesTrak (app/services/tle_downloader.py)
- Chapter 3: Parse TLE into Satellite model, extract norad_id, inclination,
  eccentricity, mean_motion, orbital_period_minutes
- Chapter 5: Skyfield orbit propagation
  - app/orbit/propagator.py
  - get_current_position(satellite) -> current lat/lon/altitude
  - get_position_at_time(satellite, time) -> position at arbitrary time
  - Both tested and working

### Next up
- Get raw XYZ position (geocentric.position.km) instead of lat/lon,
  needed for distance calculations between satellites
- Build distance function between two satellites at the same time
- This feeds into collision detection (Chapter 8)

### Not started yet
- Database (PostgreSQL) — currently nothing persists between server restarts
- Collision detection algorithm
- Risk scoring
- FastAPI endpoints beyond /satellites
- React frontend
- Scheduler for automatic background refresh