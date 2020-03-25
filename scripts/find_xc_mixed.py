import os
import csv
import pandas as pd
import shutil
def get_info(dst1, csvfile):
    cells_P_kinds = ['squamous-asc-h','squamous-asc-us','squamous-hsil','squamous-lsil']
    limit = 100
    cnt1 = 0
    cnt2 = 0
    listdst = os.listdir(dst1)
    for n in listdst:
        path_ = os.path.join(dst1, n)
        cnt1 = cnt1 + 1
        print(path_)
        dst_split = path_.split('_')
        x1 = dst_split[5]
        y1 = dst_split[6]
        x2 = dst_split[7]
        y2 = dst_split[8]
        x = int((int(x1)+int(x2))/2)
        y = int((int(y1)+int(y2))/2)
        fovname = 'IMG'+path_.split('IMG')[1].split('.jpg')[0]+'.jpg'
        reader = pd.read_csv(csvfile, index_col=None, header=0, engine='python')
        list_xc_x = (reader['x'])
        list_xc_y = (reader['y'])
        list_xc_w = (reader['w'])
        list_xc_h = (reader['h'])
        xc_fovnames = (reader['img'])
        xc_kinds = (reader['cell'])
        cnt3 = 0
        for xc_x,xc_y,xc_w,xc_h,xc_fovname,_xc_kind in zip(list_xc_x,list_xc_y,list_xc_w,list_xc_h,xc_fovnames,xc_kinds):
            xc_kind = _xc_kind.split('/')[2]
            if not xc_kind in cells_P_kinds:
                continue
            cnt3 = cnt3 + 1
            if fovname == xc_fovname:
                xc_xo = int(xc_x + xc_w/2)
                xc_yo = int(xc_y + xc_h/2)
                long_ = ((x-xc_xo)**2+(y-xc_yo)**2)**(1/2)
                if long_ < limit:
                    cnt2 = cnt2 + 1
                    print('same')
                    newpath = os.path.join('samecells', n)
                    shutil.copy(path_, newpath)
            else:
                continue
    print('阳性细胞个数，厦参阳性数量，交集数量', cnt1, cnt3, cnt2)


if __name__ == "__main__":
    dst1 = '51' #阳性细胞文件夹
    
    csvfile = '1903698_cells.csv' #厦参细胞列表
    get_info(dst1,csvfile)
