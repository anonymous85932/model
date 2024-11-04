import numpy as np
import math


# Similarity metric for two windows
def get_similarity_between_windows(window_img1, window_img2):
    sum_window_a = np.sum(window_img1)
    sum_window_b = np.sum(window_img2)
    propImg = 0.5 - (abs(sum_window_a) / (abs(sum_window_a + sum_window_b)))
    return propImg


# Similarity metric for two images
def get_similarity(img1, img2, window_size=3, signed=True):
    # Ensure the input images have the same shape
    assert img1.shape == img2.shape, "Images must have the same shape"
    # Get the shape of the images
    rows, cols = img1.shape
    # List to store computed distances for each window
    distances = []
    # Iterate over the images
    for i in range(0, rows - window_size + 1, window_size):
        for j in range(0, cols - window_size + 1, window_size):
            # Extract windows from both images
            window_img1 = img1[i:i+window_size, j:j+window_size].flatten()
            window_img2 = img2[i:i+window_size, j:j+window_size].flatten()
            # Compute the metric for the current windows and append to the list
            if np.any(window_img1) or np.any(window_img2):
                propImg = get_similarity_between_windows(
                    window_img1, window_img2)
                if not signed:
                    propImg = abs(propImg)
                distances.append(propImg)
    # Convert distances to a numpy array before computing the mean
    distances_array = np.array(distances)
    # Return the mean of all distances
    similarity = 2*np.mean(distances_array)
    if not signed:
        similarity = 1 - similarity
    return similarity


# Comparative judgement model
def comparative_judgement(sim, tau, alpha):
    # Similarity metric
    sim = sim*alpha
    # Just Noticeable Difference vector
    tau = [0, -tau, tau]
    # Normalizing factor
    norm = math.exp(0*sim - tau[0]) + math.exp(1 * sim - tau[0] -
                                             tau[1]) + math.exp(2 * sim - tau[0] - tau[1] - tau[2])
    # Expected responses
    p_left = math.exp(0*sim - tau[0]) / norm
    p_tie = math.exp(1 * sim - tau[0] - tau[1]) / norm
    p_right = math.exp(2 * sim - tau[0] - tau[1] - tau[2]) / norm
    return [p_left, p_tie, p_right]
