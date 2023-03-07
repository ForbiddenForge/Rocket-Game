WINDOW_WIDTH, WINDOW_HEIGHT = 800, 1000

LAYERS = {
    "Background Sky": 0,
    "Ground Collision": 1,
    "Ground Non-Collision": 2,
    "Ground Objects": 3,
    "Background Space 1": 4,
    "Background Space 2": 5,
    "Background Space 3": 6,
    "Clouds": 7,
    "Player": 8,
    "Map Bound": 9,
}

GRAVITATIONAL_CONSTANT = 6.6738e-11
EARTH_MASS = 5.9722e24  # kg
EARTH_RADIUS = 6.371e6  # m


# ----------------------------------------------------------------
# --------------- STAGE PARAMETERS BELOW -------------------------
# ----------------------------------------------------------------
# Parameters for Space Launch System Core Stage (Block 1, 1B & 2)
# Reference http://www.braeunig.us/space/specs/sls.htm
#                        Notes:
# Block 1 Consists of Core + SRB + ICPS + Spacecraft[payload]
# Block 1B consists of Core + SRB + Exploration Upper Stage + Spacecraft[payload]

# Dry Mass of each component
# Core Stage : 85,300 kg
# Solid Rocket Boosters : 100,390 * 2 = 200,780kg
# Interim Cryogenic Propulsion Stage : 5,000 kg
# Exploration Stage : 14,110 kg
# Total Dry Mass : 305,165 kg
# ------------------------
# Propellant Mass of each component
# Core Stage : 987,500 kg
# Solid Rocket Boosters : 631,495 * 2 = 1,262,990
# Interim Cryogenic Propulsion Stage : 28,987
# Exploration Stage : 129,000
# ------------------------
# Total Mass of each component
# Core Stage : 1,072,800 kg
# Solid Rocket Boosters : 1,463,770
# Interim Cryogenic Propulsion Stage : 33,987
# Exploration Stage : 143,110
# ------------------------
# Exhaust Velocity of each component
# Core Stage : -4292 m/s
# Solid Rocket Boosters :
# Interim Cryogenic Propulsion Stage :
# Exploration Stage : -4245 m/s
# ------------------------
# Mass Flow of each component
# Core Stage : -515 * 4 = -2060 kg/s
# Solid Rocket Boosters : -5,011.87 * 2 = -10,023.73 kg/s
# Interim Cryogenic Propulsion Stage : -25.77 kg/s
# Exploration Stage : -45 * 4 = -180 kg/s
# ------------------------
# Referance Area of each component
# Core Stage : 55.42 m**2
# Solid Rocket Boosters : 10.81 m**2
# Interim Cryogenic Propulsion Stage : 20.43 m**2
# Total Rocket Area Block 1 : 77.04 m**2
# ------------------------


CORE_STAGE = {
    "Dry Mass": 85300,
    "Propellant Mass": 987500,
    "Mass Flow": -2060,
    "Specific Impulse": 452.3,
    "Exhaust Velocity": -4292,
    "Reference Area": 77.04,
}

SOLID_ROCKET_BOOSTERS = {
    "Dry Mass": 200780,
    "Propellant Mass": 1262990,
    "Mass Flow": -10023.73,
    "Specific Impulse": 286,
    "Exhaust Velocity": -3192.42,
    "Reference Area": 10.81,
}

INTERIM_CRYOGENIC_STAGE = {
    "Dry Mass": 5000,
    "Propellant Mass": 28987,
    "Mass Flow": -25.77,
    "Specific Impulse": 462,
    "Exhaust Velocity": -4272.41,
    "Reference Area": 20.43,
    "Payload Mass": 0,
}

EXPLORATION_UPPER_STAGE = {
    "Dry Mass": 14110,
    "Propellant Mass": 129000,
    "Mass Flow": -180,
    "Specific Impulse": 0,
    "Exhaust Velocity": -2406,
    "Reference Area": 10.1,
    "Payload Mass": 0,
}

PLACE_HOLDER_STAGE = {
    "Dry Mass": 0,
    "Propellant Mass": 0,
    "Mass Flow": 0,
    "Specific Impulse": 0,
    "Exhaust Velocity": 0,
    "Reference Area": 0,
    "Payload Mass": 0,
}
