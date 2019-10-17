import pandas as pd
import os
import xmltodict, json, cv2

def get_datasets(rootpath, extension=['.png']):
    x = []
    for j in os.listdir(rootpath):
        path2 = os.path.join(rootpath, j)
        if os.path.isdir(path2):
            continue
        ext = os.path.splitext(path2)[1]
        ext = ext.lower()
        if ext in extension:
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
    dic = json.loads(jsonStr)
    return dic

def dict_to_xml(xmlpath, dic):
    with open(xmlpath, 'w') as f:
        f.write(xmltodict.unparse(dic, pretty=True))

def make_square(x1, y1, x2, y2, maxx, maxy):
    _x1, _y1, _x2, _y2 = x1, y1, x2, y2
    if (_x2 - _x1) == (_y2 - _y1):
        return _x1, _y1, _x2, _y2
    #先生成正方形坐标
    delta = (_x2 - _x1) - (_y2 - _y1)
    if delta > 0:
        _y2 = _y2 + delta
    elif delta < 0:
        _x2 = _x2 - delta
    #判断越界
    if _x2 > maxx:
        delta = _x2 - maxx
        _x1, _x2 = _x1 - delta, _x2 -delta
    if _y2 > maxy:
        delta = _y2 - maxy
        _y1, _y2 = _y1 - delta, _y2 - delta
    return _x1, _y1, _x2, _y2

if __name__ == "__main__":
    xmllists = get_datasets('./all1010', extension=['.xml'])
    total = len(xmllists)
    for i in range(total):
        xmlpath = xmllists[i]
        imgpath = xmlpath.replace('.xml', '.JPG')
        img = cv2.imread(imgpath)
        imgw, imgh, num = img.shape[1], img.shape[0], img.shape[2]

        dic = trans_xml_to_dict(xmlpath)

        #统一做成list，方便下一步遍历
        if not isinstance(dic['annotation']['object'], list):
            obj = dic['annotation']['object']
            dic['annotation']['object'] = []
            dic['annotation']['object'].append(obj)

        #target 表示要裁剪的标签
        target = ['cluster']
        for item in dic['annotation']['object']:
            if item['name'] not in target:
                continue
            x1, y1, x2, y2 = int(item['bndbox']['xmin']), int(item['bndbox']['ymin']),\
                             int(item['bndbox']['xmax']), int(item['bndbox']['ymax'])
            x1, y1, x2, y2 = make_square(x1, y1, x2, y2, imgw, imgh)
            newimg = img[y1:y2, x1:x2]
            _, shotname, _ = get_filePath_fileName_fileExt(xmlpath)
            newimgname = "{}.{}_{}_{}_{}_{}.png".format(shotname, item['name'], x1, y1, x2, y2)
            savepath = os.path.join('output', newimgname)
            cv2.imwrite(savepath, newimg)
