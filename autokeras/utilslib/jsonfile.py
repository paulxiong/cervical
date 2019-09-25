import json, glob, os
import numpy as np
import pandas as pd

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

def update_model_info_json(job):
    if os.path.exists(job.TRAINJSON) is False:
        return False
    job_info = load_json_file(job.TRAINJSON)

    mod = {}
    mod['id'] = 0
    mod['type'] = 5
    mod['did'] = job.jid
    mod['path'] = job.MODEL_DIR
    mod['desc'] = ''
    mod['recall'] = -1
    mod['precision'] = -1

    with open(job.MODJSON, 'w', encoding='utf-8') as file:
        file.write(json.dumps(mod, indent=2, ensure_ascii=False))
    return True
