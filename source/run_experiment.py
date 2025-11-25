from number_estimation import estimate_numbers, compare_numbers
from plot_results import plot_estimation_results, plot_response_distribution, plot_results_comparison
import os
import json
import datetime
import pandas as pd
from io import StringIO
import shutil


def run_experiment(
    exp_type,
    transformation,
    radius,
    radius_distribution,
    stimuli,
    repetitions,
    use_icon,
    individuals,
    filename,
    memory_images,
    memory_labels,
    iconic_memory,
    tau,
    alpha,
    memory_limit,
    stm_images,
    stm_labels,
    max_compare,
    minimum_distance,
    object_distribution
):

    image_size = 1050  # Image size in px
    window_size = [1050]  #  Window size in px for striding window
    border_distance = 0.5  # Min dist from to image to window border. 2=whole image size

    # Create a directory for the results
    date_name = datetime.datetime.now().strftime("%m%d_%H:%M:%S")
    directory_name = 'results/' + str(date_name) + " " + filename + '/'
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        
    # Check number of subdirectories in results folder
    subdir = len([x[0] for x in os.walk('results/')]) - 1
    if subdir > 100:
        dir_path = 'results/'
        subdirs = [os.path.join(dir_path, d) for d in os.listdir(
            dir_path) if os.path.isdir(os.path.join(dir_path, d))]
        sorted_subdirs = sorted(subdirs)
        for subdir in sorted_subdirs[:-10]:
            shutil.rmtree(subdir)

    # Save paramters to file
    file_path = os.path.join(directory_name, 'parameters.txt')
    with open(file_path, 'w') as file:
        for key, value in locals().items():
            file.write(f"{key} = {value}\n")

    # Number estimation
    if exp_type == 'number_estimation':

        all_results = []
        file_name_basis = directory_name

        results = estimate_numbers(N=stimuli,
                                   size=image_size,
                                   border_distance=border_distance,
                                   window_size=window_size,
                                   repetitions=repetitions,
                                   radius=radius,
                                   radius_distribution=radius_distribution,
                                   transform=transformation,
                                   object_constellation=object_distribution,
                                   minimum_distance=minimum_distance,
                                   results_directory=file_name_basis,
                                   use_icon=use_icon,
                                   individuals=individuals,
                                   memory_images=memory_images,
                                   memory_labels=memory_labels,
                                   iconic_memory=iconic_memory,
                                   tau=tau,
                                   alpha=alpha,
                                   memory_limit=memory_limit,
                                   stm_images=stm_images,
                                   stm_labels=stm_labels
                                   )
        all_results.append(results)

        # Plot results
        file_name = file_name_basis + 'estimation.png'
        file_name2 = file_name_basis + 'distribution.png'
        figy = plot_estimation_results(results, use_opacity=True, use_size=True,
                                       title_add="", label_list=[])
        figy.savefig(file_name)
        figy2 = plot_response_distribution(
            results)
        figy2.savefig(file_name2)
        csv_file_name = file_name_basis + filename + '.csv'
        json_results = json.dumps(all_results)
        json_string = json_results
        df = pd.read_json(StringIO(json_string))
        df.to_csv(csv_file_name)

    # Number Comparison
    if exp_type == 'number_comparison':

        results = compare_numbers(N=stimuli,
                                  individuals=individuals,
                                  size=image_size,
                                  border_distance=border_distance,
                                  window_size=window_size,
                                  repetitions=repetitions,
                                  radius=radius,
                                  radius_distribution=radius_distribution,
                                  transform=transformation,
                                  object_constellation=object_distribution,
                                  minimum_distance=minimum_distance,
                                  use_icon=use_icon,
                                  iconic_memory=iconic_memory,
                                  tau=tau,
                                  alpha=alpha,
                                  max_compare=max_compare)

        # Plot results
        file_name_basis = directory_name + exp_type + \
            '_radius' + str(radius)
        file_name = file_name_basis + '.png'
        file_name2 = file_name_basis + 'distribution' + '.png'
        json_file_name = file_name_basis + '.json'
        json_results = json.dumps(results)
        csv_file_name = file_name_basis + 'results.csv'
        df = pd.read_json(StringIO(json_results))
        df.to_csv(csv_file_name)
        with open(json_file_name, "w") as outfile:
            outfile.write(json_results)
        figy = plot_results_comparison(results)
        figy.savefig(file_name)
