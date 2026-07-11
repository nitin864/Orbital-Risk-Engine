from app.collision.distance import calculate_relative_velocity

vel1 = (1.73, 6.91, 1.57)
vel2 = (-2.0, 5.0, 3.0)

print(calculate_relative_velocity(vel1, vel2))