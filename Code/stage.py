from settings import *


class Stage:
    def __init__(self, dry_mass, prop_mass, mass_flow, exhaust_v, ref_area):

        self.dry_mass = dry_mass
        self.prop_mass = prop_mass
        self.mass_flow = mass_flow
        self.exhaust_velocity = exhaust_v
        self.reference_area = ref_area
        self.thrust = 0

        self.firing = True
        self.attached = True

    def check_firing(self):
        if self.firing == True:
            self.mass_flow = self.mass_flow
            self.exhaust_velocity = self.exhaust_velocity
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
        self.thrust = self.exhaust_velocity * self.mass_flow

    def update(self):
        self.check_firing()
        self.check_attachment()
        self.calc_thrust()
