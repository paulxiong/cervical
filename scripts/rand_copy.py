import os
import random
import shutil
 
def cpfile_rand(img, outfile, num):
    list_ = os.listdir(img)
    if num > len(list_):
        print('输出数量必须小于：', len(list_))
        exit()
    numlist = random.sample(range(0,len(list_)),num) # 生成随机数列表a
    cnt = 0
    for n in numlist:
        filename = list_[n]
        oldpath = os.path.join(img, filename)
        newpath = os.path.join(outfile, filename)
        shutil.copy(oldpath, newpath)
        print('剩余文件：', num-cnt)
        cnt = cnt + 1
    print('==========task OK!==========')
if __name__ == "__main__":
    cpfile_rand('img', 'outfile', 10) # 操作目录，输出目录，输出数量
