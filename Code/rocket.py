# import scrapy
import csv

import matplotlib
import mplcyberpunk
from matplotlib import pyplot as plt
from settings import *
from stage import Stage

# Use non interactive backend for matplotlib (increase performace)
matplotlib.use("agg")
plt.style.use("cyberpunk")


class Rocket:
    def __init__(self):
        self.air_density = 1.225  # kg / m**3 [rho]

        # Forces
        self.thrust = 0
        self.down_force = 0
        self.drag_force = 0
        self.resultant_force = 0

        # Update values
        self.rocket_acceleration = 0
        self.rocket_velocity = 0
        self.pos = 0
        self.delta_pos = 0

        # Values used to calculate drag force
        self.drag_coefficient = 0
        self.mach_speed = 0

        # create a dict for various params for plotting etc. later on

    def calc_mass(self, dt):
        # set propellant mass each dt minus its flow * dt
        self.core_propellant_mass = self.core_propellant_mass + self.core_mass_flow * dt
        # set the propellant mass at 0 when propellant goes negative
        self.core_propellant_mass = max(self.core_propellant_mass, 0.0)
        # update core_total_mass (total) each dt, after updating the propellant mass above
        self.core_total_mass = self.core_dry_mass + self.core_propellant_mass

    def calc_air_density(self):
        # Approximate air density based on the "U.S. Standard Atmosphere 1976" model
        # Reference: https://www.engineeringtoolbox.com/standard-atmosphere-d_604.html

        if self.pos <= 0:
            self.air_density = 1.225
        elif 0 < self.pos <= 1000:
            self.air_density = 1.112
        elif 1000 < self.pos <= 2000:
            self.air_density = 1.007
        elif 2000 < self.pos <= 3000:
            self.air_density = 0.9093
        elif 3000 < self.pos <= 4000:
            self.air_density = 0.8194
        elif 4000 < self.pos <= 5000:
            self.air_density = 0.7364
        elif 5000 < self.pos <= 6000:
            self.air_density = 0.661
        elif 6000 < self.pos <= 7000:
            self.air_density = 0.5900
        elif 7000 < self.pos <= 8000:
            self.air_density = 0.5258
        elif 8000 < self.pos <= 9000:
            self.air_density = 0.4671
        elif 9000 < self.pos <= 10000:
            self.air_density = 0.4135
        elif 10000 < self.pos <= 15000:
            self.air_density = 0.1948
        elif 15000 < self.pos <= 20000:
            self.air_density = 0.08891
        elif 20000 < self.pos <= 25000:
            self.air_density = 0.04008
        elif 25000 < self.pos <= 30000:
            self.air_density = 0.01841
        elif 30000 < self.pos <= 40000:
            self.air_density = 0.003996
        elif 40000 < self.pos <= 50000:
            self.air_density = 0.001027
        elif 50000 < self.pos <= 60000:
            self.air_density = 0.0003097
        elif 60000 < self.pos <= 70000:
            self.air_density = 0.00008283
        elif 70000 < self.pos <= 80000:
            self.air_density = 0.00001846
        elif 80000 < self.pos:
            self.air_density = 0

    def calc_drag_force(self):
        # update mach speed based from current rocket velocity
        self.mach_speed = self.rocket_velocity / 343
        # calculate drag force based loosely on the curve used in artemis simulation
        # Reference: https://www.researchgate.net/publication/362270344_Preliminary_Launch_Trajectory_Simulation_for_Artemis_I_with_the_Space_Launch_System
        if 0 > self.mach_speed <= 0.25:
            self.drag_coefficient = 0
        if 0.25 < self.mach_speed <= 1:
            self.drag_coefficient = 0.25
        elif 1.00 < self.mach_speed <= 1.25:
            self.drag_coefficient = 0.60
        elif 1.25 < self.mach_speed <= 1.5:
            self.drag_coefficient = 0.65
        elif 1.50 < self.mach_speed <= 2.00:
            self.drag_coefficient = 0.55
        elif 2.00 < self.mach_speed <= 2.25:
            self.drag_coefficient = 0.50
        elif 2.25 < self.mach_speed <= 2.50:
            self.drag_coefficient = 0.45
        elif 2.50 < self.mach_speed <= 2.75:
            self.drag_coefficient = 0.43
        elif 2.75 < self.mach_speed <= 3.00:
            self.drag_coefficient = 0.40
        elif 3.00 < self.mach_speed <= 3.50:
            self.drag_coefficient = 0.33
        elif 3.50 < self.mach_speed <= 4.00:
            self.drag_coefficient = 0.30
        elif 4.00 < self.mach_speed <= 5.00:
            self.drag_coefficient = 0.28
        elif 5.00 < self.mach_speed <= 6.00:
            self.drag_coefficient = 0.26
        elif 6.00 < self.mach_speed <= 8.00:
            self.drag_coefficient = 0.25
        elif self.mach_speed > 8:
            self.drag_coefficient = 0.23
        self.drag_force = -(
            0.5
            * self.air_density
            * (self.rocket_velocity**2)
            * self.drag_coefficient
            * self.rocket_reference_area
        )

    def calc_thrust_acc_vel(self):
        # Calculate Thrust using velocity => T = v * (dm)
        if self.core_propellant_mass > 0:
            self.thrust = self.core_exhaust_velocity * self.core_mass_flow
        else:
            self.thrust = 0
        # Newtons, listed specs for Core Stage Block 1: 7,440,000 N @ Sea Level
        # another source lists SLS as having 8.8M N
        # Note: Core stage is written to provide 25% of the thrust for the entire rocket system
        # Other stages along with their masses, thrusts, etc. are ommitted at this time.
        # Outputs are expected to have non-ideal rocket behaviour
        # ----------------------------------------------------#

        # Calculate the downward force mass * g
        self.down_force = self.core_total_mass * simple_gravity
        # Find the resultant force
        self.resultant_force = self.thrust + self.down_force + self.drag_force

        # Calculate acceleration for variable mass system => a = [resultant force] / m
        self.rocket_acceleration = self.resultant_force / self.core_total_mass

        # Use kinematics equation to update velocity
        # Second Law assumes constant "a" but with sufficiently small "dt" we can still use it
        # for a "good enough" approximation akin to Euler methods of slope approximation
        # Consider upgrading to the Rocket Equation's methodology at some point
        # and/or Runge Kutta Fourth Order [RK4]
        if self.pos == 0:
            # Prevent negative velocities while on the launch pad
            self.rocket_velocity = 0

        else:
            self.rocket_velocity = self.rocket_velocity + self.rocket_acceleration * dt

    def move(self, dt):
        # Calculate delta position[displacement s] of the rocket per dt
        self.delta_pos = self.rocket_velocity * dt + (
            0.5 * self.rocket_acceleration
        ) * (dt**2)
        # Current position = old position + delta position change [dx]
        self.pos = self.pos + self.delta_pos
        self.pos = max(self.pos, 0.0)
        print(f"Acceleration: {self.rocket_acceleration}")
        print(f"Velocity: {self.rocket_velocity}\n")
        print(f"pos: {self.pos}\n")

    def update(self, dt):
        # update method that will eventually be integrated into pygame, calling methods in their logical order to calc pos
        # and eventually move the rocket on-screen. dt is passed through as a parameter in the self.all_sprites.update(dt) call
        # in the main game loop in main.py [rocket class will be a member of the all_sprites Group]
        self.calc_mass(dt)
        self.calc_air_density()
        self.calc_drag_force()
        self.calc_thrust_acc_vel()
        self.move(dt)


# set initial time, dt, gravity, and eventually air resistance and more complex gravity
t = 0
dt = 0.1  # seconds
simple_gravity = -9.80665  # m/s**2

# Create stages and rocket object instances

core_stage = Stage(
    dry_mass=CORE_STAGE["Dry Mass"],
    prop_mass=CORE_STAGE["Propellant Mass"],
    mass_flow=CORE_STAGE["Mass Flow"],
    exhaust_v=CORE_STAGE["Exhaust Velocity"],
    ref_area=CORE_STAGE["Reference Area"],
)
srb_stage = Stage(
    dry_mass=SOLID_ROCKET_BOOSTERS["Dry Mass"],
    prop_mass=SOLID_ROCKET_BOOSTERS["Propellant Mass"],
    mass_flow=SOLID_ROCKET_BOOSTERS["Mass Flow"],
    exhaust_v=SOLID_ROCKET_BOOSTERS["Exhaust Velocity"],
    ref_area=SOLID_ROCKET_BOOSTERS["Reference Area"],
)
interim_stage = Stage(
    dry_mass=INTERIM_CRYOGENIC_STAGE["Dry Mass"],
    prop_mass=INTERIM_CRYOGENIC_STAGE["Propellant Mass"],
    mass_flow=INTERIM_CRYOGENIC_STAGE["Mass Flow"],
    exhaust_v=INTERIM_CRYOGENIC_STAGE["Exhaust Velocity"],
    ref_area=INTERIM_CRYOGENIC_STAGE["Reference Area"],
)
exploration_stage = Stage(
    dry_mass=EXPLORATION_UPPER_STAGE["Dry Mass"],
    prop_mass=EXPLORATION_UPPER_STAGE["Propellant Mass"],
    mass_flow=EXPLORATION_UPPER_STAGE["Mass Flow"],
    exhaust_v=EXPLORATION_UPPER_STAGE["Exhaust Velocity"],
    ref_area=EXPLORATION_UPPER_STAGE["Reference Area"],
)

rocket = Rocket()
# Create dictionary and associated keys for use with HUD GUI within pygame
rocket_parameters = {}
rocket_parameters["Time"] = []
rocket_parameters["Altitude"] = []
rocket_parameters["Velocity"] = []
rocket_parameters["Drag Force"] = []
rocket_parameters["Resultant Force"] = []
rocket_parameters["Acceleration"] = []
rocket_parameters["Current Total Mass"] = []
rocket_parameters["Fuel Remaining"] = []
rocket_parameters["Thrust"] = []
rocket_parameters["Down Force"] = []
rocket_parameters["Mach Speed"] = []
rocket_parameters["Air Density"] = []
rocket_parameters["Delta_pos"] = []

# Loop over rocket.update and its related methods while the rocket still has fuel
while t < 1000:
    t += 0.1

    print(f"Time is {t} seconds")
    rocket.update(dt)
    rocket.rocket_parameters["Time"].append(t)
    rocket.rocket_parameters["Fuel Remaining"].append(rocket.core_propellant_mass)
    rocket.rocket_parameters["Current Total Mass"].append(rocket.core_total_mass)
    rocket.rocket_parameters["Altitude"].append(rocket.pos)
    rocket.rocket_parameters["Velocity"].append(rocket.rocket_velocity)
    rocket.rocket_parameters["Acceleration"].append(rocket.rocket_acceleration)
    rocket.rocket_parameters["Delta_pos"].append(rocket.delta_pos)
    rocket.rocket_parameters["Thrust"].append(rocket.thrust)
    rocket.rocket_parameters["Drag Force"].append(rocket.drag_force)
    rocket.rocket_parameters["Down Force"].append(rocket.down_force)
    rocket.rocket_parameters["Resultant Force"].append(rocket.resultant_force)
    rocket.rocket_parameters["Mach Speed"].append(rocket.mach_speed)
    rocket.rocket_parameters["Air Density"].append(rocket.air_density)


# WARNING Testing purposes only!
with open("Rocket Values.csv", "w") as new_file:
    writer = csv.writer(new_file)
    key_list = list(rocket.rocket_parameters.keys())

    writer.writerow(key_list)
    writer.writerows(zip(*rocket.rocket_parameters.values()))

# scatter plot the time and specified paramater; testing purposes only before game implementation
fig1 = plt.figure()
plt.plot(
    rocket.rocket_parameters["Time"],
    rocket.rocket_parameters["Altitude"],
    label="Altitude",
)
plt.xlabel("Time")
plt.xscale("linear")
plt.ylabel("Altitude")
plt.yscale("linear")
plt.ticklabel_format(useOffset=False, style="plain")
plt.legend()
plt.grid(True)
mplcyberpunk.make_lines_glow()
plt.tight_layout()
plt.savefig("plots/Altitude.png", dpi=fig1.dpi)


# Velocity / Acceleration
fig2 = plt.figure()

plt.plot(
    rocket.rocket_parameters["Time"],
    rocket.rocket_parameters["Velocity"],
    label="Velocity",
)
plt.plot(
    rocket.rocket_parameters["Time"],
    rocket.rocket_parameters["Acceleration"],
    label="Acceleration",
)
plt.xlabel("Time")
plt.xscale("linear")
plt.ylabel("Velocity / Acceleration")
plt.yscale("linear")
plt.ticklabel_format(useOffset=False, style="plain")
plt.legend()
plt.grid(True)
mplcyberpunk.make_lines_glow()
plt.tight_layout()
plt.savefig("plots/Velocity_Acceleration.png", dpi=fig2.dpi)


# Force Plots
fig3 = plt.figure()

plt.plot(
    rocket.rocket_parameters["Time"],
    rocket.rocket_parameters["Drag Force"],
    label="Drag Force",
)
plt.plot(
    rocket.rocket_parameters["Time"],
    rocket.rocket_parameters["Down Force"],
    label="Down Force",
)
plt.plot(
    rocket.rocket_parameters["Time"], rocket.rocket_parameters["Thrust"], label="Thrust"
)
plt.plot(
    rocket.rocket_parameters["Time"],
    rocket.rocket_parameters["Resultant Force"],
    label="Resultant Force",
)
plt.xlabel("Time")
plt.xscale("linear")
plt.ylabel("Forces")
plt.yscale("linear")
plt.ticklabel_format(useOffset=False, style="plain")
plt.legend()
plt.grid(True)
mplcyberpunk.make_lines_glow()
plt.tight_layout()
plt.savefig("plots/Forces.png", dpi=fig3.dpi)
