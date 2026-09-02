# Kestrel-1 controller
# Owner: Asha

MAX_SPEED = 255


def forward(speed):
    """Drive forward at the given speed (0-255)."""
    return ("FWD", speed)


def backward(speed):
    """Drive backward at the given speed (0-255)."""
    return ("BWD", speed)


def stop():
    """Stop both motors."""
    return ("STOP", 0)


def turn_right(speed):
    """Turn right on the spot."""
    return ("RIGHT", speed)
