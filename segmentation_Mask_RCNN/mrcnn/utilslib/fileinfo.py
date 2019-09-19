import os,shutil
import pandas as pd

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

# 解析原图的文件名和文件内容, 把所有的标注全部写入一个csv
# csv的表头原图 批次  病例 原图NP 标注类型 标注NP x y
def get_info_by_FOV(origin_img_path, tocsvpath):
    lists2 = get_filelist(origin_img_path, suffix=['.jpg'])
    if lists2 is None or len(lists2) < 1:
        return False

    labels = []
    for filepath in lists2:
        if filepath is None or len(filepath) < 2:
            continue
        path1, filename, suffix1 = get_filePath_fileName_fileExt(filepath)
        csvpath = os.path.join(path1, filename + '.csv')

        arr = filename.split('.')
        if len(arr) < 4:
            print("invalied filename: %s" % filename)
            continue
        batchid, medicalid, pn = arr[0], arr[1], str(arr[2]).upper()
        filename = filename + suffix1
        #打开csv看标注的个数和类型
        df = pd.read_csv(csvpath)
        for index, row in df.iterrows():
            celltype, x, y = int(row['Type']), int(row['X']), int(row['Y'])
            cellpn = get_fov_type(str(celltype)).upper()
            labels.append([filename, batchid, medicalid, pn, celltype, cellpn, x, y])
    header = ['fov', 'batch', 'medical', 'pn', 'celltype', 'cellpn', 'x', 'y']
    pdall = pd.DataFrame(labels, columns=header)
    pdall.to_csv(tocsvpath, quoting = 1, mode = 'w', index = False, header = True)
    return True

#得到医生标注的csv，返回的是csv的全路径，仅仅是医生标注的才有csv
def get_origin_csvs(origin_imgs_dir):
    csv_lists = []
    img_lists = get_filelist(origin_imgs_dir, suffix=['.JPG', '.jpg', '.jpeg', '.png', '.PNG'])
    for i in img_lists:
        img_path, img_name, img_suffix = get_filePath_fileName_fileExt(i)
        print(img_path, img_name, img_suffix)
        csvpath = os.path.join(img_path, img_name + '.csv')
        if os.path.exists(csvpath):
            csv_lists.append(csvpath)
    return csv_lists

# 解析细胞图片文件名字，返回fov和cell的类型
def get_info_by_filename(filename):
    cell_type, fov_type, original_img_name = None, None, None

    if filename is None or len(filename) < 2:
        return fov_type, cell_type, original_img_name
    arr = filename.split('_')
    if len(arr) < 7:
        print("invalied filename: %s" % filename)
        return fov_type, cell_type, original_img_name
    cell_type = arr[2]
    fov_type = arr[1]
    return fov_type, cell_type, original_img_name

# 解析细胞图片文件名字，返回原图的名字
def get_original_imgname_by_filename(filename):
    original_img_name = None

    if filename is None or len(filename) < 2:
        return original_img_name
    arr = filename.split('_')
    if len(arr) < 2:
        print("invalied filename: %s" % filename)
        return original_img_name
    original_img_name = arr[0]
    return original_img_name

# 通过传入的细胞类型返回FOV的类型
def get_fov_type(celltype):
    p1n0 = 'p'
    n_type = ['1', '5', '12', '13', '14', '15']
    p_type = ['2', '3', '4', '6', '7', '8', '9', '10', '11']
    if celltype in n_type:
        p1n0 = 'n'
    elif celltype in p_type:
        p1n0 = 'p'
    else:
        raise RuntimeError('unkonw cell type %s' % celltype)
    return p1n0

#拷贝图片和CSV到任务目录下面
def copy_origin_imgs(filelist, imgroot, csvroot, todirroot, logger):
    if not os.path.exists(filelist):
        logger.info("not foud filelist.csv")
        return False
    for _line in open(filelist):
        line = _line.strip('\n')
        if line is None:
            continue
        arr = line.split(' ')
        if len(arr) != 3:
            logger.info("invalied filelist.csv")
            return False
        imgpath = imgroot + '/' + arr[0]
        csvpath = csvroot + '/' + arr[1]
        toimgpath = todirroot + '/' + arr[2]
        tocsvpath = toimgpath.replace('.JPG', '.csv')
        tocsvpath = tocsvpath.replace('.jpg', '.csv')

        if os.path.exists(imgpath) is False or os.path.exists(csvpath) is False:
            logger.info("file not found {} or {}".format(imgpath, csvpath))
            return False
        logger.info("cp {} {}".format(imgpath, toimgpath))
        logger.info("cp {} {}".format(csvpath, tocsvpath))
        shutil.copy(imgpath, toimgpath)
        shutil.copy(csvpath, tocsvpath)
    return True

#获得dirpath下面所有后缀是suffix的文件路径，后缀统一用小写
def get_filelist(dirpath, suffix=['.jpg']):
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
            files.append(path2)
    return files
