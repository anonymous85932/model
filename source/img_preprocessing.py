import math
import numpy as np


# Euclidean distance between two points
def coord_distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


# Find the two furthest points in a set of coordinates
def find_furthest_points(coords):
    max_distance = 0
    points = (None, None)
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            d = coord_distance(coords[i], coords[j])
            if d > max_distance:
                max_distance = d
                points = (coords[i], coords[j])
    return points


# Find the midpoint between two points
def midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]


# Translate a set of coordinates by an offset
def translate(coords, offset):
    return [[coord[0] - offset[0], coord[1] - offset[1]] for coord in coords]


# Translate a set of coordinates so that the center of mass is at the origin
def translate_to_center_of_mass(coords):
    # Compute the mean x and y coordinates
    mean_x = sum([coord[0] for coord in coords]) / len(coords)
    mean_y = sum([coord[1] for coord in coords]) / len(coords)
    # Translate so the center of mass is at the origin
    translated_coords = [[coord[0] - mean_x, coord[1] - mean_y]
                         for coord in coords]
    return translated_coords


# Rotate a set of coordinates by an angle around a center point
def rotate(coords, angle, center):
    c, s = math.cos(angle), math.sin(angle)
    new_coords = []
    for coord in coords:
        dx = coord[0] - center[0]
        dy = coord[1] - center[1]
        new_x = center[0] + c * dx - s * dy
        new_y = center[1] + s * dx + c * dy
        new_coords.append([new_x, new_y])
    return new_coords


# Scale a set of coordinates by a factor
def scale(coords, factor, center):
    new_coords = []
    for coord in coords:
        new_x = center[0] + factor * (coord[0] - center[0])
        new_y = center[1] + factor * (coord[1] - center[1])
        new_coords.append([new_x, new_y])
    return new_coords


# Mirror a set of coordinates
def mirror(coords):
    left_count = sum(1 for coord in coords if coord[0] < 0.0)
    right_count = sum(1 for coord in coords if coord[0] > 0.0)
    upper_count = sum(1 for coord in coords if coord[1] > 0.0)
    lower_count = sum(1 for coord in coords if coord[1] < 0.0)
    # Mirror horizontally if needed
    if left_count < right_count:
        coords = [[- coord[0], coord[1]] for coord in coords]
    # Mirror vertically if needed
    if upper_count < lower_count:
        coords = [[coord[0], - coord[1]] for coord in coords]
    return coords


# Stretch a set of coordinates
def stretch(coords):
    # Distance between min-x and max-x
    min_x = min([coord[0] for coord in coords])
    max_x = max([coord[0] for coord in coords])
    delta_x = max_x - min_x
    # Distance between min-y and max-y
    min_y = min([coord[1] for coord in coords])
    max_y = max([coord[1] for coord in coords])
    delta_y = max_y - min_y
    # Scale
    if (delta_y != 0):
        scale = delta_x / delta_y
        # Stretch
        coords = [[coord[0], coord[1] * scale] for coord in coords]
    # Shift coordinates so that the middle of the image is at (0,0)
    min_y = min([coord[1] for coord in coords])
    max_y = max([coord[1] for coord in coords])
    delta_y = max_y - min_y
    coords = [[coord[0] - min_x - delta_x / 2, coord[1] -
               min_y - delta_y / 2] for coord in coords]
    return coords


# Preprocess a set of coordinates
def transform_coords(coords, border_distance=0.1):
    if (len(coords) > 1):
        # Find furthest points
        p1, p2 = find_furthest_points(coords)
        mid = midpoint(p1, p2)
        # Translate so the midpoint is at the origin
        coords = translate(coords, mid)
        # Compute rotation angle
        delta_y = p2[1] - p1[1]
        delta_x = p2[0] - p1[0]
        angle = math.atan2(delta_y, delta_x)
        # Rotate points so that the furthest are horizontal
        center = [0.0, 0.0]
        coords = rotate(coords, -angle, center)
        # Scale the coordinates
        current_distance = coord_distance(p1, p2)
        desired_distance = 2-2*border_distance
        scaling_factor = desired_distance / current_distance
        coords = scale(coords, scaling_factor, center)
        # Round to 5 decimals
        coords = np.around(coords, decimals=5)
        # Mirror if necessary
        coords = mirror(coords)
        # Center points: center of mass
        coords = translate_to_center_of_mass(coords)
        if (len(coords) > 2):
            coords = stretch(coords)
    elif len(coords) == 1:
        coords[0] = (0, 0)
    return coords
