"""Ultrasonic range reader for the Kestrel-1 rover."""
from limits import SENSOR_MAX_CM, SENSOR_MIN_CM


def distance_cm(echo_us):
    """Convert an echo time in microseconds to a distance in centimetres."""
    return echo_us / 58.0


def in_range(distance):
    """True when the distance is inside the sensor's trusted range."""
    return SENSOR_MIN_CM <= distance <= SENSOR_MAX_CM
