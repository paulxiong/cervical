import pandas as pd
import os
import xmltodict, json, cv2

def get_datasets(rootpath):
    x = []
    for j in os.listdir(rootpath):
        path2 = os.path.join(rootpath, j)
        if os.path.isdir(path2):
            continue
        ext = os.path.splitext(path2)[1]
        ext = ext.lower()
        if not ext in ['.jpg', '.png', '.jpeg', '.bmp', '.JPG']:
            tmp=1
            #print(path2)
        else:
            x.append(path2)
    return x

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

def trans_xml_to_dict(xmlfile):
    xml_file = open(xmlfile, 'r')
    xml_str = xml_file.read()

    data = xmltodict.parse(xml_str)
    jsonStr = json.dumps(data, indent=2, ensure_ascii=False);
    print(jsonStr)
    dic = json.loads(jsonStr)
    for key in dic['annotation'].keys():
        print(key)

def dict_to_xml(xmlpath, dic):
    with open(xmlpath, 'w') as f:
        f.write(xmltodict.unparse(dic, pretty=True))

def get_desc(celltype):
    lists = ["", "Norm", "LSIL", "HSIL", "HPV", "NILM", "SCC", "ASCUS", \
             "ASCH", "AGC", "AIS", "ADC", "T", "M", "HSV", "X1"]
    return str(celltype) + lists[celltype]


empty = '{"annotation": {"owner": {"name": "?", "flickrid": "andrewlambie"}, "source": {"database": "The VOC2007 Database", "image": "flickr", "annotation": "PASCAL VOC2007", "flickrid": "284685227"}, "filename": "17P0603.1904869.IMG017x008.JPG", "segmented": "0", "size": {"width": 2448, "height": 2048, "depth": 3}, "object": [], "folder": "VOC2007"}}'

imglists = get_datasets('./all1010')
total = len(imglists)
for i in range(total):
    imgpth = imglists[i]
    img = cv2.imread(imgpth)
    w, h, num = img.shape[1], img.shape[0], img.shape[2]
    _, shotname, extension = get_filePath_fileName_fileExt(imgpth)

    dic = json.loads(empty)
    dic['annotation']['filename'] = shotname + extension
    dic['annotation']['size']['width'] = w
    dic['annotation']['size']['height'] = h
    dic['annotation']['size']['depth'] = num
    dic['annotation']['object'] = []
    csv = imgpth.replace('.JPG', '.csv')
    df = pd.read_csv(csv)
    objects = []
    for index, row in df.iterrows():
        celltype, x, y = int(row['Type']), int(row['X']), int(row['Y'])
        dec = get_desc(celltype)
        slid = 50
        x1 = x - slid
        x2 = x + slid
        y1 = y - slid
        y2 = y + slid
        objects.append({'name': dec, 'pose': 'Frontal', 'truncated': 0,\
                        'difficult': 0, 'bndbox': {'xmin': x1, 'ymin': y1, 'xmax': x2, 'ymax': y2}})
    if len(objects) > 0:
        dic['annotation']['object'] = objects
        xmlpath = imgpth.replace('.JPG', '.xml')
        dict_to_xml(xmlpath, dic)

    print("%d/%d %s" % (i, total, shotname))
