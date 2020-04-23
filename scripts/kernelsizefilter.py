import os, shutil

#传入文件的路径，返回路径，文件名字，文件后缀
def get_filePath_fileName_fileExt(filename):
    (filepath, tempfilename) = os.path.split(filename)
    (shotname, extension) = os.path.splitext(tempfilename)
    return filepath, shotname, extension

def parse_kernelxy_from_cellname(cellname):
    arr = cellname.split("_", -1)
    kx1, ky1, kx2, ky2 = int(arr[10]), int(arr[11]), int(arr[12]), int(arr[13])
    return kx1, ky1, kx2, ky2

def get_pid(filename):
    arr = filename.split("-", -1)
    return int(arr[1])
    
rootdir = '.'
pids = os.listdir(rootdir)
pids = sorted(pids, key=str.lower)
for i in pids:
    path1 = os.path.join(rootdir, i)
    if not os.path.isdir(path1) or i == 'valid' or i == 'invalid':
        continue
    pid = get_pid(i)
    dstpath1 = os.path.join("valid", str(pid))
    dstpath2 = os.path.join("invalid", str(pid))
    if not os.path.exists(dstpath1):
        os.makedirs(dstpath1)
    if not os.path.exists(dstpath2):
        os.makedirs(dstpath2)
    cnt = 0
    path1 = os.path.join(path1, '51')
    for j in os.listdir(path1):
        path2 = os.path.join(path1, j)
        if os.path.isdir(path2):
            continue
        filepath, shotname, extension = get_filePath_fileName_fileExt(j)
        kx1, ky1, kx2, ky2 = parse_kernelxy_from_cellname(shotname)
        w, h = (kx2 - kx1), (ky2 - ky1)
        dstpath = os.path.join(dstpath1, j)
        if (w * h) < 1100:
            dstpath = os.path.join(dstpath2, j)
            shutil.copyfile(path2, dstpath)
            continue
        #print('%d %d %d %d' % (pid, w, h, w * h))
        
        shutil.copyfile(path2, dstpath)
        cnt = cnt + 1
    print("%d,%d" % (pid, cnt))
