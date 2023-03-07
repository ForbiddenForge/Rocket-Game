
import math

theta = 90
dt = 1
acceleration = 100
velocity = 100

delta_pos_x = velocity * math.cos(theta * math.pi / 180) * dt + (0.5 * acceleration * math.cos(theta * math.pi / 180) ) * (dt**2)
delta_pos_y = velocity * math.sin(theta * math.pi / 180) * dt + (0.5 * acceleration) * (dt**2)

print(math.cos(theta * math.pi / 180))
print(delta_pos_x, delta_pos_y)
