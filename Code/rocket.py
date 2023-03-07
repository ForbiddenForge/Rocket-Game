# import scrapy

import math

import matplotlib
import mplcyberpunk
import numpy as np
import plots
from gravity import gravity_acceleration_calc
from matplotlib import pyplot as plt
from pygame import Vector2 as vector
from settings import *
from stage import Stage

# Use non interactive backend for matplotlib (increase performace)
# matplotlib.use("agg")
plt.style.use("cyberpunk")


class Rocket:
    def __init__(self):

        self.current_stage = "Core SRB"
        self.reference_area = 0
        self.air_density = 1.225  # kg / m**3 [rho]

        # List of Stage instances
        self.stage_objects = [core_stage, srb_stage, interim_stage]

        # Forces
        self.drag_force = 0

        # Update values
        self.rocket_acceleration = 0
        self.rocket_velocity = 0
        self.pos = np.array([0, 0])
        self.theta = 90

        # Values used to calculate drag force
        self.drag_coefficient = 0
        self.mach_speed = 0

    # Masses
    @property
    def total_dry_mass(self):
        return sum([stage.dry_mass for stage in self.stage_objects])

    @property
    def total_propellant_mass(self):
        return sum([stage.prop_mass for stage in self.stage_objects])

    @property
    def total_mass(self):
        return sum([stage.total_mass for stage in self.stage_objects])

    # Forces
    @property
    def weight(self):
        return self.total_mass * gravity_acceleration_calc(
            big_object_mass=EARTH_MASS,
            big_object_radius=EARTH_RADIUS,
            small_object_distance=self.pos[1],
        )

    @property
    def gravity(self):
        return -gravity_acceleration_calc(
            big_object_mass=EARTH_MASS,
            big_object_radius=EARTH_RADIUS,
            small_object_distance=self.pos[1],
        )

    @property
    def thrust(self):
        return sum([stage.thrust for stage in self.stage_objects if stage.firing])

    @property
    def resultant_force(self):
        return self.thrust + self.weight + self.drag_force

    def flight_controller(self):
        if core_stage.prop_mass > 0 and srb_stage.prop_mass > 0:
            interim_stage.firing = False
            self.current_stage = "Core SRB"
        elif srb_stage.prop_mass <= 0 and core_stage.prop_mass > 0:
            interim_stage.firing = False
            srb_stage.firing = False
            srb_stage.attached = False
            self.current_stage = "Core"
            self.theta = 150
        elif core_stage.prop_mass <= 0 and srb_stage.prop_mass <= 0:
            core_stage.firing = False
            core_stage.attached = False
            srb_stage.firing = False
            srb_stage.attached = False
            interim_stage.firing = True
            self.current_stage = "Interim"
            self.theta = 30

    def update_mass(self, dt):
        stage_dry_masses = [stage.dry_mass for stage in self.stage_objects]
        stage_prop_masses = [stage.prop_mass for stage in self.stage_objects]
        stage_total_masses = [stage.total_mass for stage in self.stage_objects]

        print(
            f"Core Stage Dry Mass: {stage_dry_masses[0]}\nCore Stage Prop Mass: {stage_prop_masses[0]}\nCore Stage Total Mass: {stage_total_masses[0]}\nSRB Stage Dry Mass: {stage_dry_masses[1]}\nSRB Stage Prop Mass: {stage_prop_masses[1]}\nSRB Stage Total Mass: {stage_total_masses[1]}\nInterim Stage Dry Mass: {stage_dry_masses[2]}\nInterim Stage Prop Mass: {stage_prop_masses[2]}\nInterim Stage Total Mass: {stage_total_masses[2]}\n"
        )

    def calc_air_density(self):
        # Approximate air density based on the "U.S. Standard Atmosphere 1976" model
        # Reference: https://www.engineeringtoolbox.com/standard-atmosphere-d_604.html
        print(f"self.pos is {self.pos}")
        print(f"self.pos[1] is {self.pos[1]}")
        if self.pos[1] <= 0:
            self.air_density = 1.225
        elif 0 < self.pos[1] <= 1000:
            self.air_density = 1.112
        elif 1000 < self.pos[1] <= 2000:
            self.air_density = 1.007
        elif 2000 < self.pos[1] <= 3000:
            self.air_density = 0.9093
        elif 3000 < self.pos[1] <= 4000:
            self.air_density = 0.8194
        elif 4000 < self.pos[1] <= 5000:
            self.air_density = 0.7364
        elif 5000 < self.pos[1] <= 6000:
            self.air_density = 0.661
        elif 6000 < self.pos[1] <= 7000:
            self.air_density = 0.5900
        elif 7000 < self.pos[1] <= 8000:
            self.air_density = 0.5258
        elif 8000 < self.pos[1] <= 9000:
            self.air_density = 0.4671
        elif 9000 < self.pos[1] <= 10000:
            self.air_density = 0.4135
        elif 10000 < self.pos[1] <= 15000:
            self.air_density = 0.1948
        elif 15000 < self.pos[1] <= 20000:
            self.air_density = 0.08891
        elif 20000 < self.pos[1] <= 25000:
            self.air_density = 0.04008
        elif 25000 < self.pos[1] <= 30000:
            self.air_density = 0.01841
        elif 30000 < self.pos[1] <= 40000:
            self.air_density = 0.003996
        elif 40000 < self.pos[1] <= 50000:
            self.air_density = 0.001027
        elif 50000 < self.pos[1] <= 60000:
            self.air_density = 0.0003097
        elif 60000 < self.pos[1] <= 70000:
            self.air_density = 0.00008283
        elif 70000 < self.pos[1] <= 80000:
            self.air_density = 0.00001846
        elif 80000 < self.pos[1]:
            self.air_density = 0

    def calc_reference_area(self):
        if self.current_stage == "Core SRB":
            self.reference_area = core_stage.reference_area
        elif self.current_stage == "Core":
            self.reference_area = core_stage.reference_area - srb_stage.reference_area
        elif self.current_stage == "Interim":
            self.reference_area = interim_stage.reference_area

    def calc_drag_force(self, dt):
        # update mach speed based from current rocket velocity
        self.mach_speed = self.rocket_velocity / 343
        # calculate drag force based loosely on the curve used in artemis simulation
        # Reference: https://www.researchgate.net/publication/362270344_Preliminary_Launch_Trajectory_Simulation_for_Artemis_I_with_the_Space_Launch_System
        if self.mach_speed <= 0.25:
            self.drag_coefficient = 0.25
        elif 0.25 < self.mach_speed <= 1:
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
        if self.rocket_velocity > 0:
            self.drag_force = -(
                0.5
                * self.air_density
                * (self.rocket_velocity**2)
                * self.drag_coefficient
                * self.reference_area
            )
            print(f"DRAG DRAG DSARG {self.drag_force}")
        else:
            self.drag_force = (
                0.5
                * self.air_density
                * (self.rocket_velocity**2)
                * self.drag_coefficient
                * self.reference_area
            )

    def calc_acc_vel(self):
        # Calculate acceleration for variable mass system => a = [resultant force] / m
        self.rocket_acceleration = self.resultant_force / self.total_mass
        print(
            f"ACCELERATION {self.rocket_acceleration}\nresultant force {self.resultant_force}\ntotal mass {self.total_mass}\n"
        )

        # Use kinematics equation to update velocity
        # Second Law assumes constant "a" but with sufficiently small "dt" we can still use it
        # for a "good enough" approximation akin to Euler methods of slope approximation
        # Consider upgrading to the Rocket Equation's methodology at some point
        # and/or Runge Kutta Fourth Order [RK4]
        # if self.pos == 0:
        #     # Prevent negative velocities while on the launch pad
        #     self.rocket_velocity = 0
        print(f"VEL BEFORE UPDATE {self.rocket_velocity}")
        self.rocket_velocity = self.rocket_velocity + self.rocket_acceleration * dt
        print(f"VEL VEL VEL {self.rocket_velocity}")

    def move(self, dt):
        # Calculate delta position[displacement s] of the rocket per dt
        # delta_pos = self.rocket_velocity * dt + (0.5 * self.rocket_acceleration) * (
        #     dt**2
        # )
        # Current position = old position + delta position change [dx]
        delta_pos_x = self.rocket_velocity * math.cos(
            self.theta * math.pi / 180
        ) * dt + (
            0.5 * self.rocket_acceleration * math.cos(self.theta * math.pi / 180)
        ) * (
            dt**2
        )

        print(f"delta pos x is {delta_pos_x}")

        delta_pos_y = self.rocket_velocity * math.sin(
            self.theta * math.pi / 180
        ) * dt + (
            0.5 * self.rocket_acceleration * math.sin(self.theta * math.pi / 180)
        ) * (
            dt**2
        )

        print(f"delta pos y is {delta_pos_y}")

        delta_pos = np.array([delta_pos_x, delta_pos_y])
        print(f"delta_pos is {delta_pos}")

        self.pos = self.pos + delta_pos
        print(f"Acceleration: {self.rocket_acceleration}")
        print(f"Velocity: {self.rocket_velocity}\n")
        print(f"pos: {self.pos}\n")
        delta_pos = 0

    def update(self, dt):
        # update method that will eventually be integrated into pygame, calling methods in their logical order to calc pos
        # and eventually move the rocket on-screen. dt is passed through as a parameter in the self.all_sprites.update(dt) call
        # in the main game loop in main.py [rocket class will be a member of the all_sprites Group]
        self.flight_controller()
        for stage in self.stage_objects:
            stage.update(dt)
        self.update_mass(dt)
        self.calc_air_density()
        self.calc_reference_area()
        self.calc_drag_force(dt)
        self.calc_acc_vel()
        self.move(dt)


# Create stages and rocket object instances using settings file


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
plots.create_rocket_dict(rocket_parameters)

# set initial time, dt, gravity, and eventually air resistance and more complex gravity
t = 0
dt = 0.1  # seconds
simple_gravity = -9.80665  # m/s**2
EARTH_MASS = 5.9722e24  # kg
EARTH_RADIUS = 6.371e6  # m


# Loop over rocket.update and its related methods while the rocket still has fuel
while t < 1000:
    t += 0.1
    # fmt: off
    print(f"Time is {t} seconds")
    rocket.update(dt)
    plots.update_rocket_dict(
        rocket_parameters=rocket_parameters, 
        t=t, 
        rocket=rocket, 
        core_stage=core_stage, 
        srb_stage=srb_stage, 
        interim_stage=interim_stage
        )


plots.csv_output(rocket_parameters)
plots.altitude_plot(rocket_parameters)
plots.position_plot(rocket_parameters)
plots.velocity_plot(rocket_parameters)
plots.acceleration_plot(rocket_parameters)
plots.force_plot(rocket_parameters)
plots.fuel_plot(rocket_parameters)
plots.drag_force_plot(rocket_parameters)
plots.weight_plot(rocket_parameters)
plots.gravity_plot(rocket_parameters)
