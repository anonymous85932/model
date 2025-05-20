import numpy as np


# Make 2D matrix of radius values
def create_radius_matrix(max_objects, test_option='increase', isPrint=False):
    if (test_option == "equal"):
        test_radius_matrix = np.tile(
            np.array([range(max_objects)]).transpose(), (1, max_objects))
    if (test_option == "increase"):
        test_radius_matrix = np.tile(
            np.array(range(max_objects)).transpose(), (max_objects, 1))
    if isPrint:
        print(test_radius_matrix)
    return test_radius_matrix
