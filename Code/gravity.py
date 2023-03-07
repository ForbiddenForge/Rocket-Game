from settings import GRAVITATIONAL_CONSTANT


def gravity_acceleration_calc(
    big_object_mass, big_object_radius, small_object_distance
):
    # Calculate the acceleration due to gravity of a large object on a small object
    # Made for universal application for different planetary bodies & objects
    gravity_acceleration = (GRAVITATIONAL_CONSTANT * big_object_mass) / (
        (big_object_radius + small_object_distance) ** 2
    )
    return -gravity_acceleration
