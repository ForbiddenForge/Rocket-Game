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
        self.rocket_velocity = 0
        self.current_velocity = 0

        self.thrust = 0
        self.down_force = 0
        self.resultant_force = 0
        self.rocket_acceleration = 0
        self.pos = 0
        self.delta_pos = 0

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
        self.resultant_force = self.thrust - self.down_force

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
        self.delta_pos = self.rocket_velocity * dt + (0.5 * self.rocket_acceleration) * (
            dt**2
        )
        # Current position = old position + delta position change [dx]
        self.pos = self.pos + self.delta_pos
        self.pos = max(self.pos, 0.0)
        # Create additional name keys with empty list values, appending vals as we loop
        print(f'Acceleration: {self.rocket_acceleration}')
        print(f"Velocity: {self.rocket_velocity}\n")
        print(f"pos: {self.pos}\n")

    def update(self, dt):
        # update method that will eventually be integrated into pygame, calling methods in their logical order to calc pos
        # and eventually move the rocket on-screen. dt is passed through as a parameter in the self.all_sprites.update(dt) call
        # in the main game loop in main.py [rocket class will be a member of the all_sprites Group]
        self.calc_mass(dt)
        self.calc_thrust_acc_vel()
        self.move(dt)


# set initial time, dt, gravity, and eventually air resistance and more complex gravity
t = 0
dt = 0.001  # seconds
simple_gravity = 9.80665  # m/s**2

# Create rocket object instance
rocket = RocketCoreStage()
rocket.rocket_parameters = {}
rocket.rocket_parameters["Fuel Remaining"] = []
rocket.rocket_parameters["Current Total Mass"] = []
rocket.rocket_parameters["time"] = []
rocket.rocket_parameters["position"] = []
rocket.rocket_parameters["velocity"] = []
rocket.rocket_parameters["acceleration"] = []
rocket.rocket_parameters["delta_pos"] = []
# Loop over rocket.update and its related methods while the rocket still has fuel
while rocket.propellant_mass > 0:
    t += 0.001

    print(f"Time is {t} seconds")
    rocket.update(dt)
    rocket.rocket_parameters["time"].append(t)
    rocket.rocket_parameters["Fuel Remaining"].append(rocket.propellant_mass)
    rocket.rocket_parameters["Current Total Mass"].append(rocket.wet_mass)
    rocket.rocket_parameters["position"].append(rocket.pos)
    rocket.rocket_parameters["velocity"].append(rocket.rocket_velocity)
    rocket.rocket_parameters["acceleration"].append(rocket.rocket_acceleration)
    rocket.rocket_parameters["delta_pos"].append(rocket.delta_pos)
    

#FIXME Testing purposes only!
# uncommenting the following line will greatly increase script run time
# print(rocket.rocket_parameters)

# scatter plot the time and specified paramater; testing purposes only before game implementation
plt.scatter(rocket.rocket_parameters["time"], rocket.rocket_parameters["position"])
plt.xlabel('Time')
plt.xscale('linear')
plt.ylabel('Altitude in Meters')
plt.yscale('linear')
plt.show()
