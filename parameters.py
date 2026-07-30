"""
Input parameters for the model.
"""

config = {
    "BOX_DIMS": (60.0, 40.0, 50.0),  # Box dimensions (X, Y, Z)
    "RECT_DIMS": (25.0, 15.0),  # Rectangle dimensions (length, width)
    "NUM_RECTANGLES": 6,  # Number of rectangles to place
    "MAX_ATTEMPTS": 100000,  # Maximum random placement attempts
    "RANDOM_SEED": 42,  # Random seed for reproducibility
    "MIN_CLEARANCE": 1.0,  # Minimum distance between rectangles, and between rectangles and box boundaries
}
