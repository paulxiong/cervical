import glob
import ntpath
import os
import shutil

import numpy as np

def process_origin_image():
    SLIDE_DIR = "datasets/" + SLIDE_NAME
    fovlist = [ item for item in os.listdir(SLIDE_DIR) if os.path.isdir(os.path.join(SLIDE_DIR, item)) ]
    for fov in fovlist:
        fov_path = os.path.join(SLIDE_DIR, fov)
        print("fov path is: ", fov_path)
        cell_folder = os.path.join(fov_path, "crops")
        celllist = np.sort(glob.glob(os.path.join(cell_folder, FILE_PATTERN)))
        if len(celllist) is 0:
            continue
        print("cell file is: ", celllist)
        for cell in celllist:
            filename = SLIDE_NAME + fov + ntpath.basename(cell)
            print("file is: ",filename)
            target_cell =  os.path.join(DST_DIR, filename)
            shutil.copy(cell, target_cell)
    
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Copy normal cells from normal slides')
        
    parser.add_argument('--origindir', required=True,
                        metavar="/path/to/origin/FOV/images/*/*...",
                        help='Directory to FOV images, for images in subdir, use */*/')
    parser.add_argument('--dstdir', required=True,
                        metavar="/path/to/segment/test/dir",
                        help='Directory of destination datasets')
    parser.add_argument('--filepattern', 
                        default='*.png',
                        metavar="file pattern to search",
                        help='file pattern to search')
    
    args = parser.parse_args()
    
    SLIDE_NAME = args.origindir
    DST_DIR = args.dstdir
    FILE_PATTERN = args.filepattern

    process_origin_image()