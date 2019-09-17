import json, glob, os
import numpy as np
from utilslib.fileinfo import get_filelist

def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def update_info_json(job):
    if os.path.exists(job.infojson) is False:
        return False

    job_info = load_json_file(job.infojson)
    job_info['origin_imgs']       = get_filelist(job.origin_imgs, suffix=['.jpg', '.JPG'])
    job_info['cells_crop']        = get_filelist(job.origin_imgs, suffix=['.jpg', '.JPG'])
    job_info['cells_crop_masked'] = get_filelist(job.origin_imgs, suffix=['.jpg', '.JPG'])
    job_info['cells_mask_npy']    = get_filelist(job.origin_imgs, suffix=['.npy'])
    job_info['cells_rois']        = get_filelist(job.origin_imgs, suffix=['.csv'])
    job_info['status'] = 2

    with open(job.infojson,'w',encoding='utf-8') as file:
        file.write(json.dumps(job_info, indent=2, ensure_ascii=False))

    return True