from run_experiment import run_experiment

# 100 ms: 21.2 & 1.2
# 500 ms: 28.0 & 1.1
# 1000 ms: 37.4 & 1.1

exp_type = "number_estimation" # "number_estimation", "number_comparison"
individuals = 100 # Number of simulated individuals
stimuli = 40 # Int. (e.g., "40" --> 1-40) or vec. (e.g., [1,5,10])
repetitions = 1 # Number of repetitions for each item / individual
max_compare = 50 # In comparison study: Max quantity of control images
radius = 10 # Radius of objects in pixels
minimum_distance = 0.05 # Min dist between objects. 2=whole image.
radius_distribution = "const" # "const" (same size), "random" (diff.  size)
use_icon = "dots" # "dots", "icons" or a file name in the icons folder
object_distribution = "uniform" # "uniform", "clustered", "homogeneous"
memory_images = [1, 2] # Quantities in LTM...
memory_labels = [1, 2] # ... and their numerals
stm_images = [] # Quantities in STM...
stm_labels = [] # ... and their numerals
iconic_memory_and_stim = [] # Iconic images in LTM & Stimuli
transformation = True # Ability to pre-process images
memory_limit = 7 # STM size limit
tau = 1.2 # Approximately: 100ms = 1.2; 500ms = 1.1, 1000m = 1.1
alpha = 21.2 # Approximately: 100ms =  21.2; 500ms =  28.0; 1000ms =  37.4
filename = "model_100ms" # Results folder name

run_experiment(exp_type,
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
               iconic_memory_and_stim,
               tau,
               alpha,
               memory_limit,
               stm_images,
               stm_labels,
               max_compare,
               minimum_distance,
               object_distribution
               )

