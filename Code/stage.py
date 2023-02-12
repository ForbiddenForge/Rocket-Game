from settings import *


class Stage:
    def __init__(self, dry_mass, prop_mass, mass_flow, exhaust_v, ref_area):

        self.dry_mass = dry_mass
        self.prop_mass = prop_mass
        self.mass_flow = mass_flow
        self.exhaust_velocity = exhaust_v
        self.reference_area = ref_area
        
        self.firing = False 
        
    def check_firing(self):
        if self.prop_mass
        
    def update(self):
        
