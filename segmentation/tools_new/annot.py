import numpy as np
import pandas as pd
import cv2
import os
import shutil
from tqdm import tqdm


def get_annot_coordinate(image, color_map):
    assert len(np.shape(image)) == 3, "Error, not supported image shape {}".format(np.shape(image))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    class_centroid = {}
    for gt in color_map.keys():
        color = color_map[gt]
        annotation = (image == color).all(axis=-1)
        if annotation.any():
            annotation = annotation.astype(np.uint8)*255
            annotation = cv2.morphologyEx(annotation, cv2.MORPH_OPEN, kernel, iterations=1)
            annotation = cv2.dilate(annotation, kernel, iterations=3)
            output = cv2.connectedComponentsWithStats(annotation)
            centroid = output[3][1:]
            class_centroid[gt] = centroid
    return class_centroid
            
def get_central_label(label_mask, class_centr):
    abnormal_labels = []
    hit_annotat = {}
    missed_annotat = {}
    for gt in class_centr.keys():
        coords = class_centr[gt].astype(np.int16)
        for centr in coords:
            #print(centr)
            label = label_mask[centr[1],centr[0]]
            #print(label.shape)
            if label != 0:
                abnormal_labels.append((label,gt))
                try:
                    hit_annotat[gt].append(centr) 
                except:
                    hit_annotat[gt] = [centr]
            else:
                try:
                    missed_annotat[gt].append(centr) 
                except:
                    missed_annotat[gt] = [centr]
    
    return abnormal_labels, hit_annotat, missed_annotat
            
def mark_missed_annotation(annotat_img, missed_centr, color_map):
    for gt in missed_centr.keys():
        coords = missed_centr[gt]
        for centr in coords:
            #print(centr)
            annotat_img = cv2.rectangle(annotat_img, tuple(centr-10), tuple(centr+10), color_map[gt], -1)
            
    return annotat_img
    
def mark_origin_fov(img, class_coords, color_map):
    for gt in class_coords.keys():
        coords = class_coords[gt]
        for centr in coords:
            #print(centr)
            annotat_img = cv2.circle(img, tuple(centr), 5, color_map[gt], -1)
    return annotat_img
    