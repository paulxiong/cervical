import json
import pandas as pd
import os
import glob
#import numpy as np
from PIL import Image, ImageDraw
from argparse
os.getcwd()

def get_files(file_path):
    cont_list = glob.glob(os.path.join(file_path,'*'))
    file_list = {}
    for content in cont_list:
        if os.path.isfile(content):
            file_list.update({os.path.basename(content):content})
        else:
            file_list.update(get_files(content))
    return file_list
    
def create_folders(save_path):
    image_path = os.path.join(save_path,'images')
    masks_path = os.path.join(save_path,'masks')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    if not os.path.exists(masks_path):
        os.makedirs(masks_path)

def get_xy(point_list):
    xy = []
    for point in point_list:
        xy.append((point['x'], point['y']))
    return xy
    
def draw_mask(size, polygon):
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).polygon(polygon, outline=255, fill=255)
    #mask = np.array(mask)
    return mask

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Tools: json to U-Net supported train set folders, with masks')
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images')
    parser.add_argument('--jsondir', required=True,
                        metavar="/path/to/json",
                        help='Directory to Segment cell images for classfication ')
    parser.add_argument('--outputdir', required=True,
                        metavar="/path/to/output",
                        help='Directory of masks outputs, absolute dir = /path/to/output')
    args = parser.parse_args()
    
    #orig_dir = '../datasets/segment/original/'
    #output_dir = '../datasets/segment/private_train'
    #json_path = './segment_label.json'
    json_path = args.jsondir
    orig_dir = args.origindir
    output_dir = args.outputdir
    
    labels = pd.read_json(json_path)
    print(labels.head())
    
    file_list = get_files(orig_dir)
    print(file_list)
    
    for i, row in labels.iterrows():
        #print(row['External ID'])
        file_name = row['External ID']
        file_path = file_list[file_name]
        file_name = file_name.split('.')[0]
        save_path = os.path.join(output_dir, file_name)
        create_folders(save_path)
        img = Image.open(file_path)
        img.save(save_path + '/images/' + file_name + '.png')
        size = img.size
        for i, polygon in enumerate(row['Label']['Nuclei']):
            point_list = polygon['geometry']
            xy = get_xy(point_list)
            mask = draw_mask(size, xy)
            mask.save(save_path + '/masks/instance_' + str(i) + '.png')