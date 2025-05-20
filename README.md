# Numerosity Estimation through comparison: Computational Models

## 1. Overview

This repository contains the codebase for a research project focused on creating computational models for how humans perceive numerosities. The primary hypothesis is that humans base their numerosity estimation on a self-correcting feedback loop based on comparative judgments.

## 2. How to run

Install dependencies:

```bash
pip3 install numpy pillow matplotlib pandas
```

To run the script, update the arguments in ./source/main.py and use the following command:

```bash
python3 ./source/main.py
```

## 3. Arguments

**STIMULI PARAMETERS**  
exp_type: # "number_estimation", "number_comparison"  
individuals: # Number of simulated individuals  
stimuli: # Int. (e.g., "40" --> 1-40) or vec. (e.g., [1,5,10])  
repetitions: # Number of repetitions for each item / individual  
max_compare: # In comparison study: Max quantity of control images  
radius: # Radius of objects in pixels  
minimum_distance: # Min dist between objects. 2=whole image  
radius_distribution: # "const" (same size), "random" (diff. size)  
use_icon: # "dots", "icons" or a file name in the icons folder  
object_distribution: # "uniform", "clustered", "homogeneous"

**MODEL PARAMETERS**  
memory_images: # Quantities in LTM...  
memory_labels: # ... and their numerals  
stm_images: # Quantities in STM...  
stm_labels: # ... and their numerals  
iconic_memory_and_stim: # Iconic images in LTM & Stimuli  
transformation: # Ability to pre-process images  
memory_limit: # STM size limit  
tau: # Approximately: 100ms = 1.2; 500ms = 1.1, 1000m = 1.1  
alpha: # Approximately: 100ms = 21.2; 500ms = 28.0; 1000ms = 37.4

**OUTPUT FOLDER**  
filename: # Results folder name

## 3. Example

exp_type = "number_estimation"  
individuals = 100  
stimuli = 40  
repetitions = 1  
max_compare = 50  
radius = 10  
minimum_distance = 0.05  
radius_distribution = "const"  
use_icon = "dots"  
object_distribution = "uniform"  
memory_images = [1, 2]  
memory_labels = [1, 2]  
stm_images = []  
stm_labels = []  
iconic_memory_and_stim = []  
transformation = True  
memory_limit = 7  
tau = 1.2  
alpha = 21.2  
filename = "model_100ms"
