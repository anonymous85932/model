import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from img_preprocessing import transform_coords
import random
import os


# Finding the minimum distance between a coordinate and a list of coordinates
def minimum_distance(coord, coords):
    distances = [((coord[0] - c[0])**2 + (coord[1] - c[1])**2)
                 ** 0.5 for c in coords]
    return min(distances)


# Create a single coordinate with a certain distance from other points
def create_x_y(coords, min_distance, border_distance):
    while True:
        # Generate a random angle
        angle = np.random.uniform(0, 2 * np.pi)
        # Sample a random area and calculate the corresponding radius
        max_area = np.pi * (1.0 - border_distance)**2
        min_area = 0
        random_area = np.random.uniform(min_area, max_area)
        radius = np.sqrt(random_area / np.pi)
        # Convert polar to Cartesian coordinates
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        # Check if this is the first point
        if not coords:
            return x, y
        at_least_one_point_is_too_close = False
        # Check distances with other points
        for c in coords:
            dist = np.sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2)
            if dist < min_distance:
                at_least_one_point_is_too_close = True
        if not at_least_one_point_is_too_close:
            return x, y


# Create coordinates with a certain number of objects
def generate_coords(num_ones, border_distance=0.05, min_distance=0.01):
    coords = []
    for _ in range(num_ones):
        # Make new point
        x, y = create_x_y(coords, min_distance, border_distance)
        # Add point to list
        coords.append([x, y])
    return [coords]


# Create clustred coordinates
def generate_clustered_coords(num_ones):
    # Set the first point, arbitrarily at (0,0)
    coords = [[0, 0]]
    # Make a dummy-list of center points in hexagonal pattern
    center_points = [
        [0.0, 0.0],    # Center point
        [10.0, 0.0],   # 1st ring
        [5.0, 8.66],
        [-5.0, 8.66],
        [-10.0, 0.0],
        [-5.0, -8.66],
        [5.0, -8.66],
        [20.0, 0.0],   # 2nd ring
        [15.0, 8.66],
        [5.0, 17.32],
        [-5.0, 17.32],
        [-15.0, 8.66],
        [-20.0, 0.0],
        [-15.0, -8.66],
        [-5.0, -17.32],
        [5.0, -17.32],
        [15.0, -8.66]
    ]
    # Start at center point
    cent = 0
    # Set current position
    currentPos = center_points[0]
    for _ in range(num_ones-1):
        # Flip a coin to decide if we should change center point
        test = np.random.random_integers(0, 2)
        if test == 0:
            cent = cent + 1
            # Update current position
            currentPos = center_points[cent % 17]
        minDist = 0
        while minDist < 2:
            rot = np.random.uniform(0, 2*np.pi)
            dist = 2
            # Update current position
            currentPos = [currentPos[0] + dist *
                          np.cos(rot), currentPos[1] + dist*np.sin(rot)]
            # Check if the new position is too close to any other position
            minDist = minimum_distance(currentPos, coords)
        # Add point to list
        coords.append(currentPos)
    return [coords]


# Create homogeneous coordinates
def generate_homogeneous_coords(num_ones):
    # Set the first point, arbitrarily at (0,0)
    coords = [[0, 0]]
    # Initiate the distance factor
    j = 0
    while len(coords) < num_ones:
        # Calculate the rest of the points
        rest = num_ones - len(coords)
        # Update the distance factor
        j = j + 1
        # Calculate the number of points in the current iteration
        ns = min(j*6, rest)
        # Update the distance factor if the rest of the points are less than one full circle
        if rest < j*6:
            j = j-1.5
        # Calculate the angular step between points in radians
        unit = 2*np.pi/ns
        # Add the points
        for k in range(ns):
            minDist = 0
            while minDist < 0.25:
                # Calculate the x and y coordinates
                x = j*np.cos(unit*k)
                y = j*np.sin(unit*k)
                # Check if the new position is too close to any other position
                minDist = minimum_distance([x, y], coords)
            # Add point to list
            coords.append([x, y])
    return [coords]


# Create grey-scale images from a certain number of objects
def create_image(n, size, border_distance, minimum_distance, object_constellation, transform, radius, radius_distribution, radius_matrix, use_icon):
    # Make coordinates from random uniform distribution
    if object_constellation == 'uniform':
        coords = generate_coords(
            n, border_distance, min_distance=minimum_distance)
    # Make clustered coordinates
    elif object_constellation == 'clustered':
        coords = generate_clustered_coords(n)
    # Make homogeneous coordinates
    elif object_constellation == 'homogeneous':
        coords = generate_homogeneous_coords(n)
    elif object_constellation == 'dice':
        if n == 1:
            coords = [[[0, 0]]]
        elif n == 2:
            coords = [[[-0.5, 0], [0.5, 0]]]
        elif n == 3:
            coords = [[[-0.5, 0], [0.5, 0], [0, 0.5]]]
        elif n == 4:
            coords = [[[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]]]
        elif n == 5:
            coords = [[[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5], [0, 0]]]
        elif n == 6:
            coords = [[[-0.5, 0], [-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0], [0.5, 0.5]]]
        else:
            coords = generate_coords(n, border_distance, min_distance=minimum_distance)
    # Preprocess coordinates
    if transform:
        coords = [transform_coords(coords[0], border_distance=border_distance)]
    # Create images from coordinates
    img = create_images_from_coords(coords, img_size=size, radius=radius,
                                    radius_distribution=radius_distribution, radius_matrix=radius_matrix, use_icon=use_icon)[0]
    return img


# Show example images in a grid
def get_fig_from_images(images):
    num_plots = len(images)
    num_cols = 5
    num_rows = int(np.ceil(num_plots / float(num_cols)))
    fig, ax = plt.subplots(num_rows, num_cols, figsize=(15, 4 * num_rows))
    ax = ax.flatten()
    for i in range(len(images)):
        img = images[i]
        ax[i].imshow(img, cmap='gray', vmin=0, vmax=1)
    plt.tight_layout()
    return fig


# Create images from coordinates
def create_images_from_coords(coords, img_size, radius, radius_distribution, radius_matrix, use_icon):
    images = []
    for coord_set in coords:
        # Initialize a black image
        # 'L': 8-bit pixels, black and white
        img = Image.new('L', (img_size, img_size), 0)
        draw = ImageDraw.Draw(img)
        # Draw circles
        if use_icon == "dots":
            # Initiate coordinate index
            for coord in coord_set:
                # Set the dotsize
                if radius_distribution == 'const':
                    radius_i = radius
                elif radius_distribution == 'random':
                    radius_i = random.randint(1, radius)
                # Set the dot position
                x = int(((coord[0] + 1) / 2) * img_size)
                y = int(((-coord[1] + 1) / 2) * img_size)
                # Set the bounding box
                bounding_box = [x-radius_i, y-radius_i, x+radius_i, y+radius_i]
                # Draw the dot
                draw.ellipse(bounding_box, fill=255, outline=None)
        # Draw icons
        if use_icon != "dots":
            # # Get the directory of the current script
            script_dir = os.path.dirname(os.path.realpath(__file__))
            # Construct the absolute path to the image file
            if use_icon == "icons":
                # Get a random file from the icons folder
                icon_files = os.listdir(
                    os.path.join(script_dir, 'stimuli_icons'))
                icon = random.choice(icon_files)
                file_path = os.path.join(
                    script_dir, 'stimuli_icons', icon)
            else:
                file_path = os.path.join(script_dir, 'stimuli_icons', use_icon)
            # Load the image
            with Image.open(file_path) as img_icon:
                for coord in coord_set:
                    # Change the icon
                    if use_icon == "icons":
                        icon_files = os.listdir(
                            os.path.join(script_dir, 'stimuli_icons'))
                        icon = random.choice(icon_files)
                        file_path = os.path.join(
                            script_dir, 'stimuli_icons', icon)
                        img_icon = Image.open(file_path)
                    # Set the icon size
                    if radius_distribution == 'const':
                        radius_i = radius
                    elif radius_distribution == 'random':
                        radius_i = random.randint(1, radius)
                    # Set the icon position
                    x = int(((coord[0] + 1) / 2) * img_size)
                    y = int(((-coord[1] + 1) / 2) * img_size)
                    # Set the bounding box and size
                    bounding_box = [x-radius_i, y -
                                    radius_i, x+radius_i, y+radius_i]
                    bounding_box_size = (
                        bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1])
                    # Resize the icon to match the size of the bounding box
                    img_icon_resized = img_icon.resize(bounding_box_size)
                    # Create a new mask image of the same size as img_icon_resized
                    mask = Image.new('L', img_icon_resized.size, 255)
                    # Paste the icon on the image
                    img.paste(img_icon_resized, bounding_box, mask)
        # Convert image to numpy array, normalize to 0-1, and append to list
        img_np = np.array(img) / 255
        images.append(img_np)
    # Convert images list to numpy array
    images = np.array(images)
    return images
