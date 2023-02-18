import csv

import matplotlib
import mplcyberpunk
from matplotlib import pyplot as plt


matplotlib.use("agg")
plt.style.use("cyberpunk")


def create_rocket_dict(rocket_parameters):
    # Create dictionary and associated keys for use with HUD GUI within pygame
    rocket_parameters["Time"] = []
    rocket_parameters["Altitude"] = []
    rocket_parameters["Velocity"] = []
    rocket_parameters["Drag Force"] = []
    rocket_parameters["Resultant Force"] = []
    rocket_parameters["Acceleration"] = []
    rocket_parameters["Current Total Mass"] = []
    rocket_parameters["Total Fuel Remaining"] = []
    rocket_parameters["Core Fuel Remaining"] = []
    rocket_parameters["SRB Fuel Remaining"] = []
    rocket_parameters["Interim Fuel Remaining"] = []

    rocket_parameters["Thrust"] = []
    rocket_parameters["Down Force"] = []
    rocket_parameters["Mach Speed"] = []
    rocket_parameters["Air Density"] = []


def update_rocket_dict(
    rocket_parameters, t, rocket, core_stage, srb_stage, interim_stage
):
    rocket_parameters["Time"].append(t)
    rocket_parameters["Total Fuel Remaining"].append(rocket.total_propellant_mass)
    rocket_parameters["Core Fuel Remaining"].append(core_stage.prop_mass)
    rocket_parameters["SRB Fuel Remaining"].append(srb_stage.prop_mass)
    rocket_parameters["Interim Fuel Remaining"].append(interim_stage.prop_mass)
    rocket_parameters["Current Total Mass"].append(rocket.total_mass)
    rocket_parameters["Altitude"].append(rocket.pos)
    rocket_parameters["Velocity"].append(rocket.rocket_velocity)
    rocket_parameters["Acceleration"].append(rocket.rocket_acceleration)
    rocket_parameters["Thrust"].append(rocket.thrust)
    rocket_parameters["Drag Force"].append(rocket.drag_force)
    rocket_parameters["Down Force"].append(rocket.weight)
    rocket_parameters["Resultant Force"].append(rocket.resultant_force)
    rocket_parameters["Mach Speed"].append(rocket.mach_speed)
    rocket_parameters["Air Density"].append(rocket.air_density)


def csv_output(rocket_parameters):
    # fmt: off
    with open("plots/Rocket Values.csv", "w") as new_file:
        writer = csv.writer(new_file)
        key_list = list(rocket_parameters.keys())

        writer.writerow(key_list)
        writer.writerows(zip(*rocket_parameters.values()))


def altitude_plot(rocket_parameters):
    # fmt: off
    fig1 = plt.figure()
    plt.plot(rocket_parameters["Time"],rocket_parameters["Current Total Mass"],label="Current Total Mass",)
    plt.plot(rocket_parameters["Time"],rocket_parameters["Altitude"],label="Altitude",)
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


def velocity_plot(rocket_parameters):
    # fmt: off
    fig2 = plt.figure()

    plt.plot(rocket_parameters["Time"], rocket_parameters["Velocity"],label="Velocity")
    plt.plot(rocket_parameters["Time"],rocket_parameters["Acceleration"],label="Acceleration",)
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


def force_plot(rocket_parameters):
    # fmt: off
    fig3 = plt.figure()

    # plt.plot(rocket_parameters["Time"],rocket_parameters["Drag Force"],label="Drag Force",)
    # plt.plot(rocket_parameters["Time"],rocket_parameters["Down Force"],label="Down Force",)
    # plt.plot(rocket_parameters["Time"], rocket_parameters["Thrust"], label="Thrust")
    plt.plot(rocket_parameters["Time"],rocket_parameters["Resultant Force"],label="Resultant Force",)
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


def fuel_plot(rocket_parameters):
    # fmt: off
    fig4 = plt.figure()

    # plt.plot(rocket_parameters["Time"],rocket_parameters["Current Total Mass"],label="Current Total Mass",)
    # plt.plot(rocket_parameters["Time"],rocket_parameters["Total Fuel Remaining"],label="Total Fuel Remaining",)
    # plt.plot(rocket_parameters["Time"],rocket_parameters["Core Fuel Remaining"] ,label="Core Fuel Remaining",)
    plt.plot(rocket_parameters["Time"],rocket_parameters["SRB Fuel Remaining"] ,label="SRB Fuel Remaining",)
    # plt.plot(rocket_parameters["Time"],rocket_parameters["Interim Fuel Remaining"] ,label="Interim Fuel Remaining",)
    plt.xlabel("Time")
    plt.xscale("linear")
    plt.ylabel("Mass")
    plt.yscale("linear")
    plt.ticklabel_format(useOffset=False, style="plain")
    plt.legend()
    plt.grid(True)
    mplcyberpunk.make_lines_glow()
    plt.tight_layout()
    plt.savefig("plots/Mass.png", dpi=fig4.dpi)


def drag_force_plot(rocket_parameters):
    # fmt: off
    fig6 = plt.figure()

    plt.plot(rocket_parameters["Time"],rocket_parameters["Drag Force"],label="Drag Force",)
    plt.xlabel("Time")
    plt.xscale("linear")
    plt.ylabel("Drag Force (N)")
    plt.yscale("linear")
    plt.ticklabel_format(useOffset=False, style="plain")
    plt.legend()
    plt.grid(True)
    mplcyberpunk.make_lines_glow()
    plt.tight_layout()
    plt.savefig("plots/DragForce.png", dpi=fig6.dpi)
