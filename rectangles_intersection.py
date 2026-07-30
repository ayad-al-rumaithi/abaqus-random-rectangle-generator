import numpy as np

def rectangles_intersection(vertices1, vertices2, min_clearance, tol=1e-8):
    """
    Determine whether two 3D rectangles violate the minimum clearance distance 
    using the Separating Axis Theorem (SAT), safely evaluating coplanar cases.

    Parameters:
        vertices1 : np.ndarray, shape (4,3)
            Coordinates of the first rectangle's vertices.
        vertices2 : np.ndarray, shape (4,3)
            Coordinates of the second rectangle's vertices.
        min_clearance : float
            Minimum acceptable spatial gap between the rectangles.
        tol : float
            Tolerance for ignoring near-zero vectors.
    """
    # Rectangle edges (vectors along sides)
    edges1 = [vertices1[1] - vertices1[0], vertices1[3] - vertices1[0]]
    edges2 = [vertices2[1] - vertices2[0], vertices2[3] - vertices2[0]]

    # Normals of rectangles (perpendicular to plane)
    normal1 = np.cross(edges1[0], edges1[1])
    normal2 = np.cross(edges2[0], edges2[1])

    # Start with standard 3D SAT base candidate axes
    axes = [normal1, normal2]
    for e1 in edges1:
        for e2 in edges2:
            axes.append(np.cross(e1, e2))

    # --- COPLANAR CHECK ---
    # If coplanar, cross-products of edges drop to zero.
    # We must inject the in-plane edge normals of BOTH rectangles to guarantee accuracy.
    cross_normals = np.cross(normal1, normal2)
    if np.linalg.norm(cross_normals) < tol:
        n_unit = normal1 / np.linalg.norm(normal1)
        for e1 in edges1:
            axes.append(np.cross(e1, n_unit))
        for e2 in edges2:
            axes.append(np.cross(e2, n_unit))

    # Single, universal loop to check separation and filter out near-zero axes
    for axis in axes:
        norm = np.linalg.norm(axis)
        if norm < tol:
            continue  # safely skip zero vectors / duplicate parallel lines
            
        axis_unit = axis / norm
        proj1 = [np.dot(v, axis_unit) for v in vertices1]
        proj2 = [np.dot(v, axis_unit) for v in vertices2]

        # Calculate the clearance gap along this projection axis
        gap = max(min(proj1) - max(proj2), min(proj2) - max(proj1))

        # If the gap along this axis is greater or equal to min_clearance, 
        # the rectangles safely satisfy the spacing constraint.
        if gap >= min_clearance:
            return False  # safe distance found → no violation

    return True  # Violation or intersection found along all axes
