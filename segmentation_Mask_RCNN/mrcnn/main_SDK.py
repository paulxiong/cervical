import os, time
import pandas as pd
from SDK.worker import worker as wk


def cell_name(datasetinfo, row):
    batchid, medicalid, imgname = str(row['batchid']), str(row['medicalid']), str(row['imgname'])
    cellname = "{}.{}.{}_{}_{}_{}_{}_x1_y1_x2_y2.png".format(
        batchid, medicalid, imgname,
        str(datasetinfo["parameter_gray"]),
        str(datasetinfo["parameter_size"]),
        str(datasetinfo["parameter_type"]),
        str(datasetinfo["parameter_mid"]))
    return cellname

if __name__ == '__main__':
    w = wk(1)
    while 1:
        #获得一个数据处理的任务
        wid, wdir = w.get_job()
        if wdir == None:
            exit()
            time.sleep(5)
            continue

        #初始化目录
        w.prepare(wid, wdir, 1)

        #读取数据集/项目信息
        dic = w.load_info_json()
        print(dic)

        columns = ['imgpath', 'p1n0', 'batchid', 'medicalid', 'imgname', 'cellpath', 'cellcached']
        cells = []

        #检查缓存目录是否有细胞缓存
        df_img = pd.read_csv(w.dataset_lists)
        for index, row in df_img.iterrows():
            batchid, medicalid, imgname = str(row['batchid']), str(row['medicalid']), str(row['imgname'])
            #print(batchid, medicalid, imgname)
            print(cell_name(dic, row))

        #df_cells = pd.DataFrame(cells, columns=['imgpath', 'batchid', 'medicalid', 'imgname', 'p1n0', ])

        #生成细胞名字和路径列表
        #save_file = df.to_csv('111.csv', quoting = 1, mode = 'w', index = False, header = True)

        #处理任务完成
        #w.done()
        w.error()
        exit()
