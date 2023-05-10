# Overview
This repository will assist you in augmenting data (cutout) for training in some cases such as object recognition with dense density, by creating a small cutout in the ground truth to simulate the overlapping of objects.


# Inference
```commandline
python cutout_aug.py --coverage_rate 0.3 --aug_number 1 --new_folder result_folder --old_folder src_folder
```
Of which, **--older_folder** is required; **--coverage_rate**, **--aug_number** and **--new_folder** are optional.

# Installation
You just need to install two libraries of Python are OpenCV and Numpy.
```commandline
pip install opencv-python
pip install numpy
```