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