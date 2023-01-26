# import scrapy
from matplotlib import pyplot as plt


class RocketCoreStage:
    def __init__(self):
        """Parameters for Space Launch System Core Stage (Block 1, 1B & 2)
        Reference http://www.braeunig.us/space/specs/sls.htm"""
        self.dry_mass = (
            85275  # kg BUG Uknown if this includes the 4 engine dry mass of 3177kg each
        )
        self.propellant_mass = 979452  # kg
        self.wet_mass = self.dry_mass + self.propellant_mass

        # RS-25D engines for the SLS (4 total)
        # Reference: https://en.wikipedia.org/wiki/RS-25
        self.mass_flow = 515 * 4  # kg /s
        self.specific_impulse = 366  # s for one engine, check if 4 engines change this
        self.exhaust_velocity = 4292  # m/s velocity of hot gasses leaving the engines

        # Other rocket parameters

        # Reference area for Block 1 Config of SLS with Core Stage[8.4m diameter], two Solid Rocket Boosters[3.71m each]
        # and Interim Cryogenic Propulsion Stage [5.1m]
        self.rocket_reference_area = 97.47  # m**2
        # TODO make a separate method for variable air density based on altitude
        self.air_density = 1.2260  # kg / m**3 [rho]

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
        self.propellant_mass = self.propellant_mass - self.mass_flow * dt
        # set the propellant mass at 0 when propellant goes negative
        self.propellant_mass = max(self.propellant_mass, 0.0)
        # update wet_mass (total) each dt, after updating the propellant mass above
        self.wet_mass = self.dry_mass + self.propellant_mass
        # Create empty lists under keys and append to these key:list as we loop
        print(
            f"Rocket Fuel Remaining {self.propellant_mass}\n",
            f"Current Total Mass {self.wet_mass}\n",
        )

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
        self.drag_force = (
            0.5
            * self.air_density
            * (self.rocket_velocity**2)
            * self.drag_coefficient
            * self.rocket_reference_area
        )

    def calc_thrust_acc_vel(self):
        # Calculate Thrust using velocity => T = v * (dm)
        if self.propellant_mass > 0:
            self.thrust = self.exhaust_velocity * self.mass_flow
        else:
            self.thrust = 0
        # Newtons, listed specs for Core Stage Block 1: 7,440,000 N @ Sea Level
        # another source lists SLS as having 8.8M N
        # Note: Core stage is written to provide 25% of the thrust for the entire rocket system
        # Other stages along with their masses, thrusts, etc. are ommitted at this time.
        # Outputs are expected to have non-ideal rocket behaviour
        # ----------------------------------------------------#

        # Calculate the downward force mass * g
        self.down_force = self.wet_mass * simple_gravity
        # Find the resultant force
        self.resultant_force = self.thrust - self.drag_force - self.down_force

        # Calculate acceleration for variable mass system => a = [resultant force] / m
        self.rocket_acceleration = self.resultant_force / self.wet_mass

        # Use kinematics equation to update velocity
        # Second Law assumes constant "a" but with sufficiently small "dt" we can still use it
        # for a "good enough" approximation akin to Euler methods of slope approximation
        # Consider upgrading to the Rocket Equation's methodology at some point
        # and/or Runge Kutta Fourth Order [RK4]
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
        self.calc_drag_force()
        self.calc_thrust_acc_vel()
        self.move(dt)


# set initial time, dt, gravity, and eventually air resistance and more complex gravity
t = 0
dt = 0.001  # seconds
simple_gravity = 9.80665  # m/s**2

# Create rocket object instance
rocket = RocketCoreStage()
# Create dictionary and associated keys for use with HUD GUI within pygame
rocket.rocket_parameters = {}
rocket.rocket_parameters["Fuel Remaining"] = []
rocket.rocket_parameters["Current Total Mass"] = []
rocket.rocket_parameters["Time"] = []
rocket.rocket_parameters["Position"] = []
rocket.rocket_parameters["Velocity"] = []
rocket.rocket_parameters["Acceleration"] = []
rocket.rocket_parameters["Delta_pos"] = []
rocket.rocket_parameters["Thrust"] = []
rocket.rocket_parameters["Drag Force"] = []
rocket.rocket_parameters["Down Force"] = []
rocket.rocket_parameters["Resultant Force"] = []
rocket.rocket_parameters["Mach Speed"] = []

# Loop over rocket.update and its related methods while the rocket still has fuel
while rocket.propellant_mass > 0:
    t += 0.001

    print(f"Time is {t} seconds")
    rocket.update(dt)
    rocket.rocket_parameters["Time"].append(t)
    rocket.rocket_parameters["Fuel Remaining"].append(rocket.propellant_mass)
    rocket.rocket_parameters["Current Total Mass"].append(rocket.wet_mass)
    rocket.rocket_parameters["Position"].append(rocket.pos)
    rocket.rocket_parameters["Velocity"].append(rocket.rocket_velocity)
    rocket.rocket_parameters["Acceleration"].append(rocket.rocket_acceleration)
    rocket.rocket_parameters["Delta_pos"].append(rocket.delta_pos)
    rocket.rocket_parameters["Thrust"].append(rocket.thrust)
    rocket.rocket_parameters["Drag Force"].append(rocket.drag_force)
    rocket.rocket_parameters["Down Force"].append(rocket.down_force)
    rocket.rocket_parameters["Resultant Force"].append(rocket.resultant_force)
    rocket.rocket_parameters["Mach Speed"].append(rocket.mach_speed)


# FIXME Testing purposes only!
# uncommenting the following lines will greatly increase script run time
# print(rocket.rocket_parameters)
# print(rocket.rocket_parameters['Thrust'])
# print(rocket.rocket_parameters["Drag Force"])
# print(rocket.rocket_parameters['Down Force'])
# print(rocket.rocket_parameters["Resultant Force"])
# print(rocket.rocket_parameters["Mach Speed"])


# scatter plot the time and specified paramater; testing purposes only before game implementation
plt.scatter(rocket.rocket_parameters["Time"], rocket.rocket_parameters["Position"])
plt.xlabel("Time")
plt.xscale("linear")
plt.ylabel("Altitude in Meters")
plt.yscale("linear")
plt.show()
