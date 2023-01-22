# import scrapy
from matplotlib import pyplot as plt


class RocketCoreStage:
    def __init__(self):
        """Parameters for Space Launch System Core Stage (Block 1, 1B & 2)
        Reference http://www.braeunig.us/space/specs/sls.htm"""
        self.dry_mass = (
            85275  # kg BUG Uknown if this includes the 4 engine dry mass of 3525kg each
        )
        self.burnout_mass = 112000  # kg maybe use later with mult stages
        self.propellant_mass = 979452  # kg
        self.wet_mass = self.dry_mass + self.propellant_mass

        # RS-25D engines for the SLS (4 total)
        # Reference: https://en.wikipedia.org/wiki/RS-25
        self.mass_flow = 515 * 4  # kg /s
        self.specific_impulse = 366  # s for one engine, check if 4 engines change this
        self.velocity_exhaust = simple_gravity * self.specific_impulse

        self.thrust = (
            self.specific_impulse
            * simple_gravity
            * 515
            * 4  # Fuel flow set at 515 kg/s per engine; total of 4 engines on the Core Stage
        )  # Newtons, listed specs for Core Stage Block 1: 7,440,000 N @ Sea Level
        # Note: Core stage is written to provide 25% of the thrust for the entire rocket system
        # Other stages along with their masses, thrusts, etc. are ommitted at this time.
        # Outputs are expected to have non-ideal rocket behaviour

        # set initial acceleration at t = 0 of acc and pos
        self.acceleration = 0
        self.pos = 0

        # create a dict for various params for plotting etc. later on
        self.rocket_parameters = {}

    def calc_mass(self, dt):
        # set propellant mass each dt minus its flow * dt
        self.propellant_mass = self.propellant_mass - self.mass_flow * dt
        # set the propellant mass at 0 when propellant goes negative
        self.propellant_mass = max(self.propellant_mass, 0.0)
        # update wet_mass (total) each dt, after updating the propellant mass above
        self.wet_mass = self.dry_mass + self.propellant_mass
        # Create empty lists under keys and append to these key:list as we loop
        self.rocket_parameters["Fuel Remaining"] = []
        self.rocket_parameters["Fuel Remaining"].append(self.propellant_mass)
        self.rocket_parameters["Current Total Mass"] = []
        self.rocket_parameters["Current Total Mass"].append(self.wet_mass)
        print(
            f"Rocket Fuel Remaining {self.propellant_mass}\n",
            f"Current Total Mass {self.wet_mass}\n",
        )

    def calc_acceleration(
        self,
    ):  # calculate acceleration using the thrust force F = ma :: a = F/m
        self.acceleration = (
            self.thrust / self.wet_mass - simple_gravity
        )  # subtract gravity for a net force; BUG unsure about this line
        print(f"Acceleration: {self.acceleration}\n")

    def move(self, dt):  # update the current velocities and position
        # v = v0 + a * dt BUG not entirely sure this is the correct eq for finding new v @ each dt
        self.velocity_exhaust = self.velocity_exhaust + self.acceleration * dt
        # Delta X = v0 * dt + 1/2(a) * dt **2
        self.delta_pos = self.velocity_exhaust * dt + 0.5 * self.acceleration * dt**2
        # Current position = old position + delta position change [dx]
        self.pos = self.pos + self.delta_pos
        # Create additional name keys with empty list values, appending vals as we loop
        self.rocket_parameters["position"] = []
        self.rocket_parameters["position"].append(self.pos)
        print(f"Velocity: {self.velocity_exhaust}\n")
        print(f"pos: {self.pos}\n")

    def update(self, dt):
        # update method that will eventually be integrated into pygame, calling methods in their logical order to calc pos
        # and eventually move the rocket on-screen. dt is passed through as a parameter in the self.all_sprites.update(dt) call
        # in the main game loop in main.py [rocket class will be a member of the all_sprites Group]
        self.calc_mass(dt)
        self.calc_acceleration()
        self.move(dt)


# set initial time, dt, gravity, and eventually air resistance and more complex gravity
t = 0
dt = 0.001  # seconds
simple_gravity = 9.80665  # m/s**2

# Create rocket object instance
rocket = RocketCoreStage()

# Loop over rocket.update and its related methods while the rocket still has fuel
while rocket.propellant_mass > 0:
    t += 0.001
    print(f"Time is {t} seconds")
    rocket.update(dt)
    # scatter plot the time and specified paramater; testing purposes only before game implementation
    plt.scatter(t, rocket.rocket_parameters["position"])


plt.show()
