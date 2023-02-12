# from pyatmos import expo

# expo_geom = expo([0, 20, 40, 60, 80])

# print(expo_geom.rho)


class MuhDick:
    def __init__(self, mydick, muhdick):
        self.dick_energy = mydick["energy"]
        self.dick_volume = mydick["volume"]
        self.dik_energy = muhdick["energy"]
        self.dik_volume = muhdick["volume"]

    def dick(self):
        big_dick_energy = self.dick_energy + self.dik_energy
        big_dick_volume = self.dick_volume + self.dik_volume
        print(big_dick_energy)
        print(big_dick_volume)


dick_dict = {"energy": 100, "volume": 300}
dik_dict = {"energy": 100, "volume": 2000}
no_dict = {"energy": 0, "volume": 0}

muh_dick = MuhDick(mydick=dick_dict, muhdick=dik_dict)
yo_dick = MuhDick(mydick=dick_dict, muhdick=no_dict)
muh_dick.dick()
yo_dick.dick()
