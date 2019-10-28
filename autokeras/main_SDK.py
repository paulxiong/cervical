import time
import pandas as pd
from SDK.worker import worker
from SDK.const.const import wt

#worker 实际需要处理的任务的函数
def worker_load(wk):
    wk.log.info(wk.cellslist_csv)
    wk.log.info(wk.datasetinfo['types'])

    types = wk.datasetinfo['types']
    if len(types) < 2 and wk.wtype == wt.TRAIN.value:
        wk.log.error("less then 2 labels to train")
        return False
    df_cells = pd.read_csv(wk.cellslist_csv)
    print(df_cells.shape)

    for i in range(100):
        #向服务器端报告任务进度
        wk.woker_percent(int(95 * i / 100), (100 - i) * 4)

        #do something
        time.sleep(1)
        return False

    return True

if __name__ == '__main__':
    w = worker(wt.TRAIN.value)
    while 1:
        wid, wdir = w.get_job()
        if wdir == None:
            exit()
            time.sleep(5)
            continue
        w.log.info("获得一个训练任务%d 工作目录%s" % (wid, wdir))

        w.prepare(wid, wdir, wt.TRAIN.value)
        w.log.info("初始化文件目录完成")

        w.datasetinfo = w.load_info_json()
        w.log.info("读取训练信息完成")

        w.log.info("开始训练")
        w.woker_percent(4, 0)
        ret = worker_load(w)

        if ret == True:
            w.done()
            w.log.info("训练完成 %d 工作目录%s" % (wid, wdir))
        else:
            w.error()
            w.log.info("训练出错 %d 工作目录%s" % (wid, wdir))
        exit()
