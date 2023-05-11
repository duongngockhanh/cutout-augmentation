# Overview
This repository will assist you in augmenting data (cutout) for training in some cases such as object recognition with dense density, by creating a small cutout in the ground truth to simulate the overlapping of objects.

![result_image](https://github.com/duongngockhanh/cutout-augmentation/assets/87640587/af9f769e-862e-481d-8d41-c5316d6a22e1)

# Inference
```commandline
python cutout_aug.py --coverage_rate 0.3 --aug_number 1 --new_folder result_folder --old_folder src_folder
```
Of which, **--older_folder** is required; **--coverage_rate**, **--aug_number** and **--new_folder** are optional.

Explanation:
- **coverage_rate**: Coverage ratio of the black box to the ground truth of the object.
- **aug_number**: The number of images created from an original image.
- **new_folder**: The folder saving new images.
- **old_folder**: The folder containing the images you want to augment.

# Installation
You just need to install two libraries of Python are OpenCV and Numpy.
```commandline
pip install opencv-python
pip install numpy
```
