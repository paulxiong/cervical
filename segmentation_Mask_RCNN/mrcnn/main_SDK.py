import time
from cells_detect_crop import cells_detect_crop

if __name__ == '__main__':
    w = cells_detect_crop()
    while 1:
        wid, wdir = w.get_job()
        if wdir == None:
            time.sleep(5)
            continue
        w.log.info("获得一个数据集预处理任务%d 工作目录%s" % (wid, wdir))

        w.prepare(wid, wdir, 1)
        w.log.info("初始化文件目录完成")

        w.datasetinfo = w.load_info_json()
        w.log.info("读取数据集信息完成")

        w.log.info("开始数据预处理, 默认ETA=1800秒")
        w.woker_percent(4, 1800)
        ret = w.crop_images()

        if ret == True:
            w.done()
            w.log.info("数据集预处理完成 %d 工作目录%s" % (wid, wdir))
        else:
            w.error()
            w.log.info("数据集预处理出错 %d 工作目录%s" % (wid, wdir))
