import os,shutil

# 解析文件名字，返回fov和cell的类型
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

# 解析文件名字，返回原图的名字
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