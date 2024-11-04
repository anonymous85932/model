# Numerosity Estimation through comparison: Computational Models

## 1. Overview

This repository contains the codebase for a research project focused on creating computational models for how humans perceive numerosities visually. The primary hypothesis is that humans base their numerosity estimation on a self-correcting feedback loop based on visual imagery.

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
exp_type: The experimental type: _Discrimination_ or _estimation_.  
individuals: The Number of simulated individuals.  
stimuli: Quantities in the stimuli set.  
repetitions: The number of repetitions for each item / individual.  
max_compare: If a comparative design: The max quantities with which quantities are compared.  
radius: The radius of objects in pixels.  
minimum_distance: Minimum distance between objects. The whole frame is 2 units.  
radius_distribution: Whether objects in stimuli should have constant or random size.  
use_icon: Whether stimuli should be iconic or dots.  
object_distribution: How the objects are structured.

**MODEL PARAMETERS**  
memory_images: The quantities of LTM Images.  
memory_labels: The labels of these images.  
stm_images: The quantities of STM Images.  
stm_labels: The labels of these images.  
iconic_memory_and_stim: The quantities of iconic images stored in LTM and shown in stimuli.  
transformation: The ability to pre-process images.  
memory_limit: The size of STM.  
tau: Threshold parameter. The amount of information a person needs before considering two stimuli as sufficiently similar.  
alpha: Discrimination parameter. The amount of information an individual extracts from the input.

**OUTPUT FOLDER**  
filename: Extention to the output filename.

## 3. Example

1. A simulation of human estimation:
   **exp_type** = "number_estimation"
2. Simulates a human study with 100 participants:
   **individuals** = 100
3. With stimuli quantities 1-20:
   **stimuli** = 20
4. And each quantity is repeated 5 times (with a new image for each repetition).
   **repetitions** = 5
5. The (base) radius of the objects is 10px.
   **radius** = 10
6. The minimum distance between the objects is 0.05, ensuring that, in the current setting, no objects overlap.
   **minimum_distance** = 0.05.
7. And all objects have this exact radius.
   **radius_distribution** = "const"
8. The objects are selected randomly from the .png - images stored in the "stimuli_icons" folder.
   **use_icon** = "icons"
9. The icons are clustred.
   **object_distribution** = "clustered"
10. Each individual have in his/her LTM one perfect representation of images containing 1, 2, and 3 objects. In addition, each individual has three different representations of images containing 4 objects.
    **memory_images** = [1, 2, 3, 4, 4, 4]
11. All of these images are represented by their true/correct labels.
    **memory_labels** = [1, 2, 3, 4, 4, 4]
12. Each individual has before the trials been shown an image containing 60 objects (i.e., this image is contained in STM).
    **stm_images** = [60]
13. But each individual falsely beleive that this image is a representation of 50 objects.
    **stm_labels** = [50]
14. In addition to the other images stored in LTM, each individual has iconic representations of images containing 6 and 7 objects. Also, whenever a stimuli contains 6 or 7 objects, the stimuli will show these exact images.
    **iconic_memory_and_stim** = [6, 7]
15. Each individual has the general ability of preprocessing mental images (e.g., scale and rotate).
    **transformation** = True
16. The STM limit for each individual is 7 objects.
    **memory_limit** = 7
17. Each individual has _tau_ parameter of 1.
    **tau** = 1
18. Each individual has an alpha parameter of 20.
    **alpha** = 20
19. The output files are saved in the results folder with a filname starting with datetime followed by "estimation100ms".
    **filename** = "estimation100ms"
