import time

from matplotlib import pyplot as plt


class Rocket:
    def __init__(self):
        self.pos = 0  # m
        self.delta_pos = 0

        self.initial_vel = 0  # m/s
        self.vel = 2400  # m/s
        self.delta_vel = 0

        self.initial_acc = 0
        self.acc = 0  # m/s**2

        self.rocket_mass = 187566  # kg
        self.initial_fuel_mass = 2591394
        self.fuel_mass = 2591394  # kg
        self.payload_mass = 21040  # kg
        self.initial_total_mass = (
            self.rocket_mass + self.payload_mass + self.initial_fuel_mass
        )
        self.burn_rate = 14000  # kg/s

        self.reference_area = 10  # m**2 front of rocket
        self.drag_coef = 0.5

        self.rocket_parameters = {}
        self.rocket_parameters["Time"] = []
        self.rocket_parameters["Altitude"] = []

    def calc_total_mass(self, dt):
        self.fuel_mass = self.initial_fuel_mass - 1400 * dt
        if self.fuel_mass > 0:
            self.total_mass = self.rocket_mass + self.payload_mass + self.fuel_mass
        else:
            self.total_mass = self.rocket_mass + self.payload_mass
            self.fuel_mass = 0
        print(
            f"Rocket total mass is: {self.total_mass}\n Fuel remaining: {self.fuel_mass}\n DT is {dt}\n"
        )

    def calc_rocket_acc(self, dt):
        self.acc = (self.vel / self.total_mass) * (self.burn_rate) - simple_gravity
        self.delta_vel = self.acc * dt
        self.vel = self.initial_vel + self.delta_vel
        print(f"Rocket Acceleration: {self.acc}\n Rocket Velocity: {self.vel}")

    def update_rocket_pos(self, dt):
        self.delta_pos = ((self.initial_vel + self.delta_vel) / 2) * dt
        self.pos += self.delta_pos
        print(f"Rocket height: {self.pos} meters\n\n\n")
        print("--------------------------------------------")

    def launch_rocket(self, dt):
        self.rocket_parameters["Time"].append(dt)
        self.calc_total_mass(dt)
        self.calc_rocket_acc(dt)
        self.update_rocket_pos(dt)
        self.rocket_parameters["Altitude"].append(round(rocket.pos))

    def run(self):
        for dt in range(0, 10):
            print(dt)
            self.launch_rocket(dt)


iss_altitude = 355000  # 355km in m
radius_earth = 6.37 * 10**6  # m
simple_gravity = 9.81

dt = 1

rocket = Rocket()
rocket.run()


print(rocket.rocket_parameters["Altitude"])
plt.plot(rocket.rocket_parameters["Time"], rocket.rocket_parameters["Altitude"])
plt.show()
