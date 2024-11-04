from collections import Counter
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt


# Plot response distribution
def plot_response_distribution(results):
    results = [t[:3] for t in results]
    # Dictionary to keep track of frequency of prev_m values for each n.
    data_dict = {}
    for n, prev_m, _ in results:
        if n not in data_dict:
            data_dict[n] = {}
        if prev_m not in data_dict[n]:
            data_dict[n][prev_m] = 0
        data_dict[n][prev_m] += 1
    # Create a single figure with multiple subplots
    num_plots = len(data_dict)
    num_rows = int(np.ceil(num_plots / 3.0))
    fig, axs = plt.subplots(num_rows, 3, figsize=(15, 4 * num_rows))
    axs = axs.flatten()
    if num_plots == 1:
        axs = [axs]
    # Plot
    i = 0
    for ax, (n, prev_m_dict) in zip(axs, data_dict.items()):
        i += 1
        if (n < max(data_dict.keys()) + 2):
            x = list(prev_m_dict.keys())
            y = list(prev_m_dict.values())
            ax.bar(x, y, label='Model data')
            ax.set_title(f'n = {n}', y=0.5)
            ax.set_xlabel('Estimated number')
            ax.set_ylabel('%')
            # ax.set_xlim(0, 20)  # Explicitly set x-axis range
            ax.set_ylim(0, 100)
            ax.set_xticks(range(0, max(x), 5))
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            if i == 1:
                ax.legend()
    return fig


# Plot comparison results
def plot_results_comparison(results_list):
    fig = plt.figure()
    if not isinstance(results_list[0], list):
        results_list = [results_list]
    for results in results_list:
        control_nums = [res[0] for res in results]
        compare_nums = [res[1] for res in results]
        comparison_ratio = [res[2] for res in results]
        labely = str(control_nums[0])
        plt.plot(compare_nums, comparison_ratio, '-', label=labely)
    plt.xlabel('Img 2')
    plt.ylabel('Greater-response ratio')
    titly = 'Discrimination ratio'
    plt.title(titly)
    plt.legend()
    leg = plt.legend()
    leg.set_title('Img 1')
    return fig


# Colormap
def get_colors_from_colormap(n, colormap_name="viridis"):
    # Get the colormap
    colormap = cm.get_cmap(colormap_name)
    # Generate n evenly spaced values between 0 and 1
    values = np.linspace(0, 0.8, n)
    # Get the colors from the colormap
    colors = [colormap(value) for value in values]
    return colors


# Plot estimation results
def plot_estimation_results(results_list, use_opacity=True, use_size=True, title_add="", label_list=[]):
    fig = plt.figure()
    results_list = [t[:3] for t in results_list]
    if not isinstance(results_list[0], list):
        results_list = [results_list]
    if len(label_list) != len(results_list):
        label_list = ['Model data']*len(results_list)
    model_results_length = len(results_list)
    color_list = get_colors_from_colormap(
        len(results_list), colormap_name='cividis')
    color_index = 0
    for results in results_list:
        control_nums = [res[0] for res in results]
        compare_nums = [res[1] for res in results]
        # Count repetitions
        counts = Counter([(x, y) for x, y in zip(control_nums, compare_nums)])
        unique_points = list(counts.keys())
        counts_values = list(counts.values())
        max_count = max(counts_values)
        base_size = 30
        # Opacity
        if use_opacity:
            opacities = [1 * (count / max_count) for count in counts_values]
        else:
            opacities = [1] * len(unique_points)
        # Size
        if use_size:
            sizes = [1 * (count / max_count) *
                     base_size for count in counts_values]
        else:
            sizes = [base_size]*len(unique_points)
        # Plot scatter plot
        if color_index < model_results_length:
            i = 0
            for (x, y), _ in zip(unique_points, counts_values):
                plt.scatter(
                    x, y, s=sizes[i], color=color_list[color_index], alpha=[opacities[i]])
                i += 1
        # Plot the standard deviation:
        # Group by x-values
        grouped_data = {}
        for x, y, z in results:
            if x not in grouped_data:
                grouped_data[x] = []
            grouped_data[x].append(y)
        # Calculate mean and standard deviation for each group
        x_vals = []
        y_means = []
        y_stds = []
        y_medians = []
        for x, ys in grouped_data.items():
            x_vals.append(x)
            y_means.append(np.mean(ys))
            y_stds.append(np.std(ys))
            y_medians.append(np.median(ys))
        # Plotting
        alpha = 0.4
        plt.errorbar(x_vals, y_means, yerr=y_stds, fmt='-', capsize=3,
                     color=color_list[color_index], label=label_list[color_index], alpha=alpha)
        color_index += 1
    # Plotting the identity function
    max_n, max_m = max_values_from_triplets(results)
    max_n_m = min(max_n, max_m)
    plt.plot([0, max_n_m], [0, max_n_m], 'k-')
    plt.xlabel('Presented number')
    plt.ylabel('Estimated number')
    title = 'Number estimation: ' + title_add
    plt.title(title)
    plt.legend()
    return fig


# Get the max value from a triplet
def max_values_from_triplets(triplets):
    # Unzip the triplets using the zip function and the * operator
    first_elements, second_elements, _ = zip(*triplets)
    # Return the maximum values from the first and second elements
    return max(first_elements), max(second_elements)
