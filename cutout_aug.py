import os
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--coverage_rate', type=float, default=0.3, help="coverage rate to each bounding box")
parser.add_argument('--aug_number', type=int, default=2, help="the number of new image after augmenting data")
parser.add_argument('--new_folder', type=str, default="result", help="the result folder")
parser.add_argument('--old_folder', type=str, required=True, help="the source folder")
opt = parser.parse_args()

def xywh2xyxy(x, y, w, h):
    xmin = int(x - w/2)
    ymin = int(y - h/2)    
    xmax = int(x + w/2)
    ymax = int(y + h/2)
    return xmin, ymin, xmax, ymax

def yolo2xywh(w_img, h_img, yolo_label):
    x_box = yolo_label[0] * w_img
    y_box = yolo_label[1] * h_img
    w_box = yolo_label[2] * w_img
    h_box = yolo_label[3] * h_img
    return x_box, y_box, w_box, h_box

def spawn_coverage(img, coverage_rate, x_box, y_box, w_box, h_box):
    w_coverage_min = int(coverage_rate * w_box)
    w_coverage = np.random.randint(w_coverage_min, w_box) # random value 1
    h_coverage = int(h_box * (coverage_rate / (w_coverage/w_box)))
    xmin, ymin, xmax, ymax = xywh2xyxy(x_box, y_box, w_box, h_box)

    coverage_point_index = np.random.randint(0, 4) # random value 2
    if coverage_point_index == 0:
        xmin_coverage, ymin_coverage = xmin, ymin
        xmax_coverage, ymax_coverage = xmin + w_coverage, ymin + h_coverage
    elif coverage_point_index == 1:
        xmin_coverage, ymin_coverage = xmax - w_coverage, ymin
        xmax_coverage, ymax_coverage = xmax, ymin + h_coverage
    elif coverage_point_index == 2:
        xmin_coverage, ymin_coverage = xmax - w_coverage, ymax - h_coverage
        xmax_coverage, ymax_coverage = xmax, ymax
    else:
        xmin_coverage, ymin_coverage = xmin, ymax - h_coverage
        xmax_coverage, ymax_coverage = xmin + w_coverage, ymax

    img = cv2.rectangle(img, (xmin_coverage, ymin_coverage), (xmax_coverage, ymax_coverage), color=(0, 0, 0), thickness=-1)
    return img

def draw_coverage(img, lbl_path):
    # take the labels from txt file
    boxes_info = []
    with open(lbl_path) as file:
        for line in file:
            lbl_info = line.strip().split()
            box_info = list(map(float,lbl_info[1:]))
            boxes_info.append(box_info)

    # draw for each label
    w_img, h_img, _ = img.shape
    for yolo_label in boxes_info:
        x_box, y_box, w_box, h_box = yolo2xywh(w_img, h_img, yolo_label)
        img = spawn_coverage(img, coverage_rate, x_box, y_box, w_box, h_box)
    return img

def copy_txt_content(old_txt_path, new_txt_path):
    with open(old_txt_path) as old_file:
        content = old_file.read()
    with open(new_txt_path, "w") as new_file:
        new_file.write(content)

if __name__ == "__main__":
    coverage_rate = opt.coverage_rate
    aug_number = opt.aug_number
    new_folder = opt.new_folder
    old_folder = opt.old_folder

    # make a new folder to save the result
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)

    # read the data in a folder
    for ele_file in os.listdir(old_folder):
        if ele_file.endswith(".jpg") or ele_file.endswith(".png"):
            no_extension = ele_file[:-4] # the name of the file that not contain the extension
            img_path = os.path.join(old_folder, ele_file)
            lbl_path = os.path.join(old_folder, no_extension + ".txt")
            inital_img = cv2.imread(img_path)

            for ele_new in range(1, aug_number + 1):
                img = inital_img.copy()
                img = draw_coverage(img, lbl_path)

                new_ele_file = no_extension + '_' + str(ele_new)
                new_img_path = os.path.join(new_folder, new_ele_file + ".jpg")
                cv2.imwrite(new_img_path, img)
                new_lbl_path = os.path.join(new_folder, new_ele_file + ".txt")
                copy_txt_content(lbl_path, new_lbl_path)