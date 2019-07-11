import json, glob, os
import numpy as np

def get_path(paths, prefix):
    if len(paths) < 1:
        return paths
    ret_paths = []
    for i in paths:
        ret_paths.append(i[len(prefix)+1:])
    return ret_paths

def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def step7v2(job):
    if os.path.exists(job.infojson) is False:
        return False

    job_info = load_json_file(job.infojson)
    job_info['input_datasets_img']        = get_path(glob.glob(os.path.join(job.input_datasets + '/*/', "*.JPG")), job.jobdir)
    job_info['input_datasets_csv']        = get_path(glob.glob(os.path.join(job.input_datasets + '/*/', "*.csv")), job.jobdir)
    job_info['input_datasets_denoising']  = get_path(glob.glob(os.path.join(job.input_datasets_denoising + '/*/*/', "*.png")), job.jobdir)
    job_info['middle_mask']               = get_path(glob.glob(os.path.join(job.middle_mask + '/' + 'predict/test/colour' + '/*/', "*.png")), job.jobdir)
    job_info['output_datasets_crop']      = get_path(glob.glob(os.path.join(job.output_datasets + '/*output/' + 'crops/' + '*.png')), job.jobdir)
    job_info['output_datasets_npy']       = get_path(glob.glob(os.path.join(job.output_datasets_npy + '/' + '*.png')), job.jobdir)
    job_info['output_datasets_slide_npy'] = get_path(glob.glob(os.path.join(job.output_datasets_slide_npy + '/' + '*.npy')), job.jobdir)
    job_info['status'] = 2

    with open(job.infojson,'w',encoding='utf-8') as file:
        file.write(json.dumps(job_info, indent=2, ensure_ascii=False))

    return True
