import os, json, shutil, cv2

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

def load_json_file(filepath):
    load_dict = ''
    with open(filepath, 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    return load_dict

def get_json_lists(testdir):
    dir_or_files = os.listdir(testdir)
    imgs = []
    for i in dir_or_files:
        path1 = os.path.join(testdir, i)
        ext = os.path.splitext(path1)[1]
        ext = ext.lower()
        if not ext in ['.json']:
            continue
        imgs.append(path1)
    return imgs

def copy_valid_invalid(jsonfilepath, valid_str):
    _, shotname, extension = get_filePath_fileName_fileExt(jsonfilepath)
    dst = "result/" + valid_str + "/" + shotname
    filepath = jsonfilepath.replace(".json", "", -1)
    shutil.copyfile(filepath, dst)
    return

def copy_valid(jsonfilepath):
    copy_valid_invalid(jsonfilepath, "valid")
    return

def copy_invalid(jsonfilepath):
    copy_valid_invalid(jsonfilepath, "invalid")
    return

copyvalid = False
jsons = get_json_lists("./1211_gray/invalid")
for i in jsons:
    dic = load_json_file(i)
    cntk, cntm = 0, 0

    filepath, shotname, extension = get_filePath_fileName_fileExt(i)
    imgpath = os.path.join(filepath, shotname)
    original_image = cv2.imread(imgpath)
    for j in dic.keys():
        w, h, score, classname = dic[j]["w"], dic[j]["h"], dic[j]["score"], dic[j]["class"]
        x1, y1, x2, y2 = dic[j]["x1"], dic[j]["y1"], dic[j]["x2"], dic[j]["y2"]
        if classname == 'kernel':
            cntk = cntk + 1
        elif classname == 'mid':
            cntm = cntm + 1
        txt = str(int(score*100)) + classname
        cv2.rectangle(original_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
        if classname == 'kernel':
            cv2.putText(original_image, txt, (int(x1), int(y1)), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1)
    out_img = str(imgpath) + ".yolo.png"

    #个数检查
    if cntk < 1 or (cntk + cntm) >= 5 or cntm >=2 :
        print("1invalid %s" % i)
        copy_invalid(i)
        if copyvalid:
            cv2.imwrite(out_img, original_image)
        continue

    #得分检查, 大于70分能够基本保留valid，valid只删除了51个
    invalid = True
    for j in dic.keys():
        score, classname = dic[j]["score"], dic[j]["class"]
        if classname != 'kernel':
            continue
        if int(score*100) >= 80:
            invalid = False
            break
    if invalid is True:
        print("2invalid %d %s" %(int(score*100), i))
        copy_invalid(i)
        if copyvalid:
            cv2.imwrite(out_img, original_image)
        continue

    #长宽检查
    invalid = True
    wh_threhold = 9
    for j in dic.keys():
        w, h, classname = dic[j]["w"], dic[j]["h"], dic[j]["class"]
        if classname != 'kernel':
            continue
        if w > wh_threhold and h > wh_threhold:
            invalid = False
            break
        if w < wh_threhold or h < wh_threhold:
            invalid = True
        print(w, h)
    if invalid is True:
        print("3invalid %s" % i)
        copy_invalid(i)
        if copyvalid:
            cv2.imwrite(out_img, original_image)
        continue

    #没滤掉，说明是好细胞
    copy_valid(i)
    for j in dic.keys():
        score = dic[j]["score"]
        w, h = dic[j]["w"], dic[j]["h"]
        print("4valid %d w=%d h=%d %s" %(int(score*100), w, h, i))
    if not copyvalid:
        cv2.imwrite(out_img, original_image)
