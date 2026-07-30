import numpy as np

def rectangles_vertices(center, width, height, rotation_matrix):
    """
    Compute the 4 vertices of a rectangle in 3D space given its center, dimensions, and rotation.

    Parameters:
        center : list or array-like [x, y, z]
            The rectangle's center coordinates.
        width, height : float
            Rectangle dimensions along local X, Y axes.
        rotation_matrix : np.ndarray, shape (3,3)
            Rotation applied to the rectangle (local → global coordinates).

    Returns:
        np.ndarray, shape (4,3)
            Array of 3D coordinates for each rectangle vertex.
    """
    dx, dy = width / 2.0, height / 2.0

    # Define vertices in rectangle's local reference frame (z=0)
    local_coords = np.array([
        [-dx, -dy, 0],
        [ dx, -dy, 0],
        [ dx,  dy, 0],
        [-dx,  dy, 0]
    ])

    # Apply rotation
    rotated = (rotation_matrix @ local_coords.T).T
    # Translate to global coordinates
    translated = rotated + np.array(center)

    return translated