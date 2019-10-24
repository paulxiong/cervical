import os, time
import pandas as pd
from SDK.worker import worker as wk

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

        #检查缓存目录是否有细胞缓存
        df = pd.read_csv(w.dataset_lists)
        for index, row in df.iterrows():
            batchid, medicalid, imgname = str(row['batchid']), str(row['medicalid']), str(row['imgname'])
            print(batchid, medicalid, imgname)
        exit()
