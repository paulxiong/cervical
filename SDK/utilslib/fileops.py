import json, os

#把json文件读到内存为dict
def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def getcellname(batchid, medicalid, imgid, imgname, gray, size, _type, mid, x1, y1, x2, y2, celltype):
    cellname = "{}.{}.{}.{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.png".format(
        batchid, medicalid, imgid, imgname,
        str(gray), str(size), str(_type), str(mid),
        x1, y1, x2, y2, celltype)
    return cellname

def parse_imgid_xy_from_cellname(cellname):
    arr = cellname.split("_", -1)
    x1, y1, x2, y2 = int(arr[5]), int(arr[6]), int(arr[7]), int(arr[8])
    arr = cellname.split(".", -1)
    imgid = int(arr[2])

    return imgid, x1, y1, x2, y2


def get_file_lists(dirpath, suffix=['.png']):
    dir_or_files = os.listdir(dirpath)
    imgs = []
    for i in dir_or_files:
        path1 = os.path.join(testdir, i)
        ext = os.path.splitext(path1)[1]
        ext = ext.lower()
        if not ext in suffix:
            continue
        imgs.append(path1)
    return imgs
