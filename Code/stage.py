from pygame import Vector2 as vector
from settings import *
from gravity import gravity_acceleration_calc


class Stage:
    def __init__(self, dry_mass, prop_mass, mass_flow, exhaust_v, ref_area):

        self.dry_mass = dry_mass
        self.prop_mass = prop_mass
        self.total_mass = dry_mass + prop_mass

        self.mass_flow = mass_flow
        self.mass_flow_copy = mass_flow
        self.exhaust_velocity = exhaust_v
        self.exhaust_velocity_copy = exhaust_v
        self.reference_area = ref_area
        self.thrust = 0

        self.firing = True
        self.attached = True

    def calc_mass(self, dt):
        # Update propellant mass and total mass per delta time
        self.prop_mass = self.prop_mass + self.mass_flow * dt
        self.prop_mass = max(self.prop_mass, 0.0)
        self.total_mass = self.prop_mass + self.dry_mass
        self.total_mass = max(self.total_mass, 0.0)

    def check_firing(self):
        # Since later stage firings are set to False at outset, need a backup value to repeg to once they begin firing
        # TODO find a better method of solving this logic
        if self.firing == True:
            self.mass_flow = self.mass_flow_copy
            self.exhaust_velocity = self.exhaust_velocity_copy
        else:
            self.mass_flow = 0
            self.exhaust_velocity = 0

    def check_attachment(self):
        if self.attached == True:
            self.dry_mass = self.dry_mass
            self.reference_area = self.reference_area
        else:
            self.dry_mass = 0
            self.reference_area = 0

    def calc_thrust(self):
        # Calculate Thrust using velocity => T = v * (dm)
        self.thrust = (
            self.exhaust_velocity * self.mass_flow if self.prop_mass > 0 else 0
        )

    def update(self, dt):
        self.calc_mass(dt)
        self.check_firing()
        self.check_attachment()
        self.calc_thrust()
