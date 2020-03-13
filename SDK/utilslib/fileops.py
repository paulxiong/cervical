import json, os

#把json文件读到内存为dict
def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def getcellname(batchid, medicalid, imgid, imgname, gray, size, _type, mid, x1, y1, x2, y2, celltype, kx1, ky1, kx2, ky2):
    cellname = "{}.{}.{}.{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.png".format(
        batchid, medicalid, imgid, imgname,
        str(gray), str(size), str(_type), str(mid),
        x1, y1, x2, y2, celltype, kx1, ky1, kx2, ky2)
    return cellname

def parse_kernelxy_from_cellname(cellname):
    arr = cellname.split("_", -1)
    kx1, ky1, kx2, ky2 = int(arr[10]), int(arr[11]), int(arr[12]), int(arr[13])
    return kx1, ky1, kx2, ky2

def parse_imgid_xy_from_cellname(cellname):
    arr = cellname.split("_", -1)
    x1, y1, x2, y2 = int(arr[5]), int(arr[6]), int(arr[7]), int(arr[8])
    arr = cellname.split(".", -1)
    imgid = int(arr[2])
    return imgid, x1, y1, x2, y2

def get_file_lists(dirpath, suffix=['.png']):
    imgs = []
    dirs = os.listdir(dirpath)
    for i in dirs:
        path1 = os.path.join(dirpath, i)
        if not os.path.isdir(path1):
            continue
        dir_or_files = os.listdir(path1)
        for j in dir_or_files:
            path2 = os.path.join(path1, j)
            if os.path.isdir(path2):
                continue
            ext = os.path.splitext(path2)[1]
            ext = ext.lower()
            if not ext in suffix:
                continue
            imgs.append(path2)
    return imgs
