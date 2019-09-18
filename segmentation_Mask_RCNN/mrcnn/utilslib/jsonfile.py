import json, glob, os
import numpy as np

#获得目录里面的文件，返回的路径以jobdir开始，目的是给前端显示
#startdir表示要删除的路径的前面
#比如原始路径/ai/thumbor/data/loader/scratch/DksFBjRO/origin_imgs/17P0603=1903805=P=IMG006x009.JPG
#前端实际显示时候只需要DksFBjRO/origin_imgs/17P0603=1903805=P=IMG006x009.JPG
#startdir就是/ai/thumbor/data/loader/scratch/
def _get_filelist(dirpath, startdir, suffix=['.jpg']):
    files = []
    if not os.path.isdir(dirpath):
        return files
    for j in os.listdir(dirpath):
        path2 = os.path.join(dirpath, j)
        if os.path.isdir(path2):
            continue
        ext = os.path.splitext(path2)[1]
        ext = ext.lower()
        if not ext in suffix:
            # print("skip %s" % path2)
            continue
        else:
            files.append(path2[len(startdir):])
    return files

def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def update_info_json(job, status):
    if os.path.exists(job.infojson) is False:
        return False

    startdir = os.path.join(job.scratchdir) + '/'
    job_info = load_json_file(job.infojson)
    job_info['origin_imgs']       = _get_filelist(job.origin_imgs, startdir, suffix=['.jpg', '.JPG', '.png'])
    job_info['cells_crop']        = _get_filelist(job.crop, startdir, suffix=['.jpg', '.JPG', '.png'])
    job_info['cells_crop_masked'] = _get_filelist(job.crop_masked, startdir, suffix=['.jpg', '.JPG', '.png'])
    job_info['cells_mask_npy']    = _get_filelist(job.mask_npy, startdir, suffix=['.npy'])
    job_info['cells_rois']        = _get_filelist(job.rois, startdir, suffix=['.csv'])
    job_info['status'] = status

    with open(job.infojson,'w',encoding='utf-8') as file:
        file.write(json.dumps(job_info, indent=2, ensure_ascii=False))

    return True