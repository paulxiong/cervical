# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:27:04 2019

@author: hjj
"""
import os, json, xmltodict, cv2

def get_datasets(rootpath, extension=['.png']):
    x = []
    for j in os.listdir(rootpath):
        path2 = os.path.join(rootpath, j)
        if os.path.isdir(path2):
            continue
        ext = os.path.splitext(path2)[1]
        ext = ext.lower()
        if ext in extension:
            x.append(j)
    return x

def dict_to_xml(xmlpath, dic):
    with open(xmlpath, 'w') as f:
        f.write(xmltodict.unparse(dic, pretty=True))

def get_classes(filelists):
    dic = {}
    for i in filelists:
       strs = i.split("_", -1)
       imgname = strs[0].replace(".cluster", "")
       imgname = imgname.replace(".good", "")

       img_path = 'all1010_1018'
       path = os.path.join(img_path , imgname+'.JPG')
       org_img = cv2.imread(path)

       save_path = './org_img'
       save_path = os.path.join(save_path, imgname + '.JPG')
       cv2.imwrite(save_path , org_img )

       if imgname not in dic.keys():
           dic[imgname] = {}

       typename = strs[0].split(".", -1)[2]
       if typename not in dic[imgname].keys():
           dic[imgname][typename] = []

       x1, y1, x2, y2 = int(strs[1]), int(strs[2]), int(strs[3]), strs[4]
       y2 = int(y2.replace(".png", ""))
       dic[imgname][typename].append({'name': typename, 'pose': 'Frontal', 'truncated': 0, 'difficult': 0, 'bndbox': {'xmin': x1, 'ymin': y1, 'xmax': x2, 'ymax': y2}})
    return dic

arr = get_datasets('output/', extension=['.png'])
dic = get_classes(arr)
empty = '{"annotation": {"owner": {"name": "?", "flickrid": "andrewlambie"}, "source": {"database": "The VOC2007 Database", "image": "flickr", "annotation": "PASCAL VOC2007", "flickrid": "284685227"}, "filename": "17P0603.1904869.IMG017x008.JPG", "segmented": "0", "size": {"width": 2448, "height": 2048, "depth": 3}, "object": [], "folder": "VOC2007"}}'


for key in dic.keys():
    xml_dic = json.loads(empty)
    xml_dic['annotation']['filename'] = key
    xml_dic['annotation']['size']['width'] = 100
    xml_dic['annotation']['size']['height'] = 100
    xml_dic['annotation']['size']['depth'] = 3
    xml_dic['annotation']['object'] = []

    for key2 in dic[key].keys():
        for i in dic[key][key2]:
            xml_dic['annotation']['object'].append(i)

    dict_to_xml(key + ".xml", xml_dic)






