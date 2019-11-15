import json

#把json文件读到内存为dict
def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def getcellname(batchid, medicalid, imgname, gray, size, _type, mid, x1, y1, x2, y2, celltype):
    cellname = "{}.{}.{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.png".format(
        batchid, medicalid, imgname,
        str(gray), str(size), str(type), str(mid),
        x1, y1, x2, y2, celltype)
    return cellname

def parse_xy_from_cellname(cellname):
    arr = cellname.split("_", -1)
    x1, y1, x2, y2 = int(arr[5]), int(arr[6]), int(arr[7]), int(arr[8])
    return x1, y1, x2, y2
