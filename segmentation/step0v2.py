import os,shutil

def step0v2(filelist, imgroot, csvroot, todirroot, logger):
    for _line in open(filelist):
        line = _line.strip('\n')
        if line is None:
            print(line)
        arr = line.split(' ')
        if len(arr) != 3:
            logger.info("invalied filelist.csv")
            return False
        imgpath = imgroot + '/' + arr[0]
        csvpath = csvroot + '/' + arr[1]
        dirpath = todirroot + '/' + arr[2]

        if os.path.exists(imgpath) is False or os.path.exists(csvpath) is False:
            logger.info("file not found {} or {}".format(imgpath, csvpath))
            return False
        if os.path.exists(dirpath) is False:
            os.makedirs(dirpath)
        logger.info("cp {} {}".format(imgpath, dirpath))
        logger.info("cp {} {}".format(csvpath, dirpath))
        shutil.copy(imgpath, dirpath)
        shutil.copy(csvpath, dirpath)
    return True
