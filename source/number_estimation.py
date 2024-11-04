from create_images import create_image, get_fig_from_images
from distance_measures import get_similarity, comparative_judgement
from radius_matrix import create_radius_matrix
import numpy as np
import random
import time
import sys


# Show example images
def get_fig_from_example_images(n_objects_list, image_generation_args):
    images = []
    for n_objects in n_objects_list:
        img = create_image(
            n_objects, *image_generation_args)
        images.append(img)
    fig = get_fig_from_images(images)
    return fig


# Time left function for progress bar
def format_time_left(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return f"{int(days)}d {int(hours)}h {int(mins)}m"
    elif hours > 0:
        return f"{int(hours)}h {int(mins)}m"
    else:
        return f"{int(mins)}m"


# Progress bar
def print_progress_bar(n_i, total, start_time, length=50):
    progress = n_i / total
    block = int(length * progress)
    bar = "█" * block + "-" * (length - block)

    elapsed_time = time.time() - start_time
    if n_i > 0:
        estimated_total_time = elapsed_time * (total / n_i)
        time_left = estimated_total_time - elapsed_time
    else:
        time_left = 0
    time_left_str = format_time_left(time_left)
    sys.stdout.write(
        f"\rProgress: |{bar}|  {progress * 100:.1f}%  Time left: {time_left_str}     ")
    sys.stdout.flush()


# Number estimation function
def estimate_numbers(N,
                     size,
                     border_distance,
                     window_size,
                     repetitions,
                     radius,
                     radius_distribution,
                     transform,
                     object_constellation,
                     minimum_distance,
                     results_directory,
                     use_icon,
                     individuals,
                     memory_images,
                     memory_labels,
                     iconic_memory,
                     tau,
                     alpha,
                     memory_limit,
                     stm_images,
                     stm_labels
                     ):

    # If N is a list, then the range is defined by N.
    # Otherwise the range is defined by range(1,N+1)
    if isinstance(N, list):
        rangy = N
        n_m_max = max(N)
    else:
        rangy = range(1, N+1)
        n_m_max = N

    # Set window-size
    if isinstance(window_size, list):
        window_size_list = window_size
    else:
        window_size_list = [window_size]

    # Create and save example images as example_images.png
    radius_matrix = create_radius_matrix(
        n_m_max, test_option='increase', isPrint=False)
    n_objects_list = [1, 2, 3, 4, 5, 10, 20,
                      30, 40, 50, 110, 120, 130, 140, 150]
    image_generation_args = (size, border_distance, minimum_distance, object_constellation,
                             transform, radius, radius_distribution, radius_matrix, use_icon)
    fig = get_fig_from_example_images(
        n_objects_list, image_generation_args)
    example_image_file_path = results_directory + 'example_images.png'
    fig.savefig(example_image_file_path)

    # Make list of iconic images with labels
    iconic_images = []
    for i in range(len(iconic_memory)):
        img = create_image(iconic_memory[i], size, border_distance, minimum_distance, 'dice', transform, radius, radius_distribution, radius_matrix, use_icon)
        iconic_images.append(img)

    # Initiate memory
    memory_max = memory_limit + len(iconic_memory) + len(memory_images)
    # Add LTM images to memory
    mem_img = memory_images[:]
    mem_lbl = memory_labels[:]
    # Add STM images to memory
    for i in range(len(stm_images)):
        mem_img.append(stm_images[i])
        mem_lbl.append(stm_labels[i])

    # Empty array for results
    results = []
    # Initial direction for the estimate
    initial_direction = 'none'
    # Simulation ID name
    id = 1000
    n_i = -1
    # Set start time for progress bar
    start_time = time.time()

    # sets rangy to repetitions*randomized range,
    # e.g. rangy = [1, 2, 3], repetitions=3 could return --> [2, 1, 3, 1, 2, 3, 3, 1, 2]
    rangy = [*rangy]
    repeated_random_range = []
    for _ in range(repetitions):
        random.shuffle(rangy)
        repeated_random_range.extend(rangy)
    rangy = repeated_random_range

    # Start Estimation Trial for Every Individual
    for _ in range(individuals):
        random.shuffle(rangy)
        # Set ID for the simulation
        id += 1
        n_i += 1

        # Update progress bar
        time.sleep(0.1)
        print_progress_bar(n_i, individuals, start_time)

        # Clear memory
        memory_images = []
        memory_labels = []
        memory_true = []

        # Add LTM to memory
        for i in range(len(mem_img)):
            img = create_image(mem_img[i], size, border_distance, minimum_distance, 'uniform',
                               transform, radius, radius_distribution, radius_matrix, use_icon)
            memory_images.append(img)
            memory_labels.append(mem_lbl[i])
            memory_true.append(mem_img[i])

        # Add the iconic images to memory
        for i in range(len(iconic_memory)):
            img = iconic_images[i]
            memory_images.append(img)
            memory_labels.append(iconic_memory[i])
            memory_true.append(iconic_memory[i])

        # Add STM to Memory
        for i in range(len(stm_images)):
            img = create_image(stm_images[i], size, border_distance, minimum_distance, 'uniform',
                               transform, radius, radius_distribution, radius_matrix, use_icon)
            memory_images.append(img)
            memory_labels.append(stm_labels[i])
            memory_true.append(stm_images[i])

        # Start Estimation Trials
        item_index = 0
        for n in rangy:
            item_index += 1
            # If memory is full, remove the oldest item
            if len(memory_images) > memory_max:
                memory_images.pop(-(memory_limit + 1))
                memory_labels.pop(-(memory_limit + 1))
                memory_true.pop(-(memory_limit + 1))

            # Load n-th stimulus

            # If the n-th stimulus is in the iconic memory, load it from there...
            if n in iconic_memory:
                control_img = iconic_images[iconic_memory.index(n)]
                # ...else, create the n-th stimulus
            else:
                control_img = create_image(n, size, border_distance, minimum_distance,
                                           object_constellation, transform, radius, radius_distribution, radius_matrix, use_icon)

            # Check memory for best match
            similarity_match = []
            # For every item in Memory, compare it to the control image and store the similarity
            for item in memory_images:
                compare_img = item
                similarity = 0
                for window_size_i in window_size_list:
                    greater_smaller_measure_i = get_similarity(
                        control_img, compare_img, window_size=window_size_i, signed=True)
                    similarity += greater_smaller_measure_i
                similarity /= len(window_size_list)
                similarity_match.append(similarity)

            # Get the place in the list of the most similar image
            closest_match = np.argmin(np.abs(similarity_match))

            # Get the image (closest match) from memory
            best_image = memory_images[closest_match]
            # ... and its label
            m = memory_labels[closest_match]

            # Reset the direction for the estimate
            direction = initial_direction

            # Start estimation loop
            stop = False
            time_used = 0
            add_to_memory = True

            while (stop == False):
                time_used += 1  # Increase the computation time with 1 unit
                # If the label is represented in the memory: use that image...
                if m in memory_labels and add_to_memory == True:
                    compare_img = best_image[:]
                    add_to_memory = False
                else:
                    # ... if not: Simulate a new image
                    compare_img = create_image(m, size, border_distance, minimum_distance,
                                               object_constellation, transform, radius, radius_distribution, radius_matrix, use_icon)
                    add_to_memory = True

                # Get similarity between control and compare image
                similarity = 0
                for window_size_i in window_size_list:
                    greater_smaller_measure_i = get_similarity(
                        control_img, compare_img, window_size=window_size_i, signed=True)
                    similarity += greater_smaller_measure_i
                similarity /= len(window_size_list)

                # Get judgment (True if similar)
                smaller_tie_larger = comparative_judgement(
                    similarity, tau, alpha)
                choices = ['smaller', 'tie', 'larger']
                smaller_tie_larger_sample = random.choices(
                    choices, weights=smaller_tie_larger, k=1)[0]
                decision_criterion = smaller_tie_larger_sample == 'tie'

                # Set direction for next trial
                if smaller_tie_larger_sample == 'smaller':
                    direction = "up"
                if smaller_tie_larger_sample == 'larger':
                    direction = "down"

                # If similar: STOP, store the result...
                if decision_criterion:
                    if direction == "up":
                        result_m = m - 1
                    if direction == "down":
                        result_m = m + 1
                    result_m = m
                    results.append((n, result_m, similarity, id, time_used, item_index))

                    # ... and add the estimate to STM
                    if (add_to_memory == True):
                        memory_images.append(control_img)
                        memory_labels.append(m)
                        memory_true.append(n)
                    break

                # If not similar, continue with next trial
                if direction == "none":
                    m = m
                if direction == "up":
                    m += 1
                if direction == "down":
                    m -= 1
                    if m == 0:
                        m = 1
    # Print progress bar
    time.sleep(0.1)
    print_progress_bar(n_i+1, individuals, start_time)
    print()

    # Write results
    results.sort(key=lambda x: x[0])
    return results


def compare_numbers(N,
                    individuals,
                    size,
                    border_distance,
                    repetitions,
                    radius,
                    radius_distribution,
                    transform,
                    object_constellation,
                    window_size,
                    minimum_distance,
                    use_icon,
                    iconic_memory,
                    tau,
                    alpha,
                    max_compare
                    ):

    # Empty array for results
    results = []

    # Maximum number of objects the stimuli are compared to
    max_compare = max_compare + 1

    # If N is a list, then the range is defined by N.
    # Otherwise the range is defined by range(1,N+1)
    if isinstance(N, list):
        n_range = N
        max_n_list = max(N)
        n_m_max = max(max_n_list, max_compare)
    else:
        n_range = range(1, N+1)
        n_m_max = max(N, max_compare)

    # Matrix for image generation
    radius_matrix = create_radius_matrix(
        n_m_max, test_option='increase', isPrint=False)

    # Initiate time counter for progress bar
    total_iterations = len(n_range) * individuals * \
        repetitions * (max_compare - 1)
    n_i = 0

    # Set timer for progress bar
    start_time = time.time()

    # Start comparison trials
    for n in n_range:
        results_n = []
        m_range = range(1, max_compare)
        for m in m_range:
            comparative_judgment = []
            for _ in range(repetitions*individuals):

                # Generate Img 1
                control_img = create_image(n, size, border_distance, minimum_distance,
                                           object_constellation, transform, radius, radius_distribution, radius_matrix,
                                           use_icon)
                # Generate Img 2
                compare_img = create_image(m, size, border_distance, minimum_distance,
                                           object_constellation, transform, radius, radius_distribution, radius_matrix,
                                           use_icon)

                # Set window-size
                if isinstance(window_size, list):
                    window_size_list = window_size
                else:
                    window_size_list = [window_size]

                # Get similarity between Img 1 and Img 2
                similarity = 0
                for window_size_i in window_size_list:
                    greater_smaller_measure_i = get_similarity(
                        control_img, compare_img, window_size=window_size_i, signed=True)
                    similarity += greater_smaller_measure_i
                similarity /= len(window_size_list)

                # Get comparative judgment
                smaller_tie_larger = comparative_judgement(
                    similarity, tau=tau, alpha=alpha)
                choices = [0, 1, 2]
                smaller_tie_larger_sample = random.choices(
                    choices, weights=smaller_tie_larger, k=1)[0]
                comparative_judgment.append(smaller_tie_larger_sample)

                # Update time counter and progress bar
                n_i += 1
                print_progress_bar(n_i, total_iterations, start_time)
            # Mean of comparative judgments
            estimated_jugment = np.mean(comparative_judgment)
            results_n.append((n, m, estimated_jugment))
        # Write results
        results.append(results_n)
    # Print progress bar
    print()

    return results
