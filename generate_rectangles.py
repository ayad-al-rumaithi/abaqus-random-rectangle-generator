import random
import math
import numpy as np

from rotation_matrix_zxz import rotation_matrix_zxz
from rectangles_vertices import rectangles_vertices
from rectangles_intersection import rectangles_intersection

def generate_rectangles(config):
    """
    Generate non-overlapping, randomly rotated rectangles inside a 3D box.

    Parameters:
        config : dict
            Configuration dictionary containing box/rectangle dimensions,
            count, maximum attempts, random seed, and minimum clearance.

    Returns:
        list of tuples: (center, (alpha, beta, gamma), vertices)
            Center coordinates, ZXZ Euler angles (degrees), and vertex coordinates.
    """
    # Extract parameters from the config dictionary
    BOX_W, BOX_H, BOX_D = config["BOX_DIMS"]
    RECT_W, RECT_H = config["RECT_DIMS"]
    num_rectangles = config["NUM_RECTANGLES"]
    max_attempts = config["MAX_ATTEMPTS"]
    random_seed = config["RANDOM_SEED"]
    min_clearance = config["MIN_CLEARANCE"]

    random.seed(random_seed)
    np.random.seed(random_seed)

    rectangle_data = []
    attempts = 0

    while len(rectangle_data) < num_rectangles and attempts < max_attempts:
        attempts += 1

        # Random ZXZ Euler angles
        alpha = random.uniform(0, 360)
        gamma = random.uniform(0, 360)
        beta = math.degrees(math.acos(2*random.random() - 1))  # uniform sphere rotation

        R = rotation_matrix_zxz(alpha, beta, gamma)

        # Random rectangle center inside the box
        center = (
            random.uniform(0, BOX_W),
            random.uniform(0, BOX_H),
            random.uniform(0, BOX_D)
        )

        # Compute rotated vertices
        vertices = rectangles_vertices(center, RECT_W, RECT_H, R)

        # Check if rectangle satisfies clearance with box boundaries
        box_limit = np.array([BOX_W, BOX_H, BOX_D])
        if np.any(vertices.min(axis=0) < min_clearance) or np.any(vertices.max(axis=0) > (box_limit - min_clearance)):
            continue

        # Check intersection and clearance with previously placed rectangles
        if any(rectangles_intersection(vertices, placed, min_clearance) for _, _, placed in rectangle_data):
            continue

        rectangle_data.append((center, (alpha, beta, gamma), vertices))

    print(f"Placed {len(rectangle_data)} rectangles after {attempts} attempts.")
    return rectangle_data
