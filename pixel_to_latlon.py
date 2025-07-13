import numpy as np
import math
import cv2


def geodetic_to_ecef(lat_deg, lon_deg, h):
    # WGS84 ellipsoid constants
    a = 6378137.0  # semi-major axis, meters
    e2 = 6.69437999014e-3  # first eccentricity squared

    # convert degrees → radians
    phi = math.radians(lat_deg)
    lam = math.radians(lon_deg)

    # prime‐vertical radius of curvature
    N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)

    # ECEF coordinates
    X = (N + h) * math.cos(phi) * math.cos(lam)
    Y = (N + h) * math.cos(phi) * math.sin(lam)
    Z = (N * (1 - e2) + h) * math.sin(phi)

    return X, Y, Z


if __name__ == "__main__":
    pass