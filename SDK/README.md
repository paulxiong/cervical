#### 1 简介
每个后台的数据处理/训练/预测进程是一个worker，SDK提供一个worker实例的基本配置、常用函数、向后端请求任务、统计系统状态的方法。
SDK提供的是框架，改变算法或者处理流程，SDK不需要改变。
```
              <------- 任务按顺序放队列里面, 任务可以手动提高优先级来插队(还没做)
              ┏━━━━┯━━━━┯━━━━━━━┯━━━━┓
              ┃job1┃job2┃  ...  ┃jobn┃
              ┗━━━━┷━━━━┷━━━━━━━┷━━━━┛
              ^
              │  取任务, 执行任务
              │
┏━━━━━━━┯━━━━━━━┯━━━━━━━┯━━━━━━━┓
┃worker1┃worker2┃  ...  ┃workern┃
┃━━━━━━━┼━━━━━━━┼━━━━━━━┼━━━━━━━┃
┃  CPU  ┃  GPU1 ┃CPU/GPU┃  GPU2 ┃
┗━━━━━━━┷━━━━━━━┷━━━━━━━┷━━━━━━━┛

```

#### 2 数据约定
##### 数据目录
```
├── csv    存放医生标注的csv，有数据库的情况这个目录没用，信息都在数据库里面
│   └── 17P0603
│       ├── 2019-7-22
│       │   ├── 1904165A
│       │   │   ├── IMG001x008.csv
│
├── img   存放原图
│   └── 17P0603
│       ├── 1904165A
│       │   ├── Images
│       │   │   ├── IMG001x008.JPG
│
├── scratch
│   ├── 17P0603  #切割的缓存
│   │   ├── 1904165A
│   │   │   ├── cells
│   │   │   │   ├── IMG001x008.JPG
│   │
│   ├── data       这个表示这里存的是数据
│   │   ├── img2
│   │   │   └── cells
│   │   │       ├── 批次         如果是用户上传的，批次就是时间+用户id
│   │   │       │   ├── 病例_x_y_w_h_color_slid_csv_mod.png
│   │
│   ├── img   存放用户通过web上传的图片
│   │   └── b157262400000013     批次ID,'b'+天的时间戳+用户ID
│   │       ├── m157268362091213 病历号,'m'+当前秒的时间戳+用户ID
│   │       │   ├── Images
│   │       │   │   ├── IMG001x008.JPG 用户上传的图片的名字
│   │
│   ├── review   存放审核细胞的原图和细胞图
│   │   ├── img     原图目录
│   │   └── cell    细胞目录
│
├── datasets           这个和数据库的datasets概念一致, 只存放了一个文件列表及说明
│   ├── DkxD9Kjl   workdir
│   │   ├── info.json    数据集的描述文件
│   │   ├── info2.json    数据集的描述文件,裁剪完之后的统计
│   │   ├── filelist.csv 前端需要用到的datasets的原图列表
│   │   ├── cellslist.csv 细胞图列表
│
├── projects          每新建一个项目，对应的文件系统产生一个这个目录
│   ├── qXTqpz6P
│   │   ├── info.json    前端传来的参数
│   │   ├── lists.json   前端需要用到的datasets的列表, 包括带缓存的和不带缓存的, 不带缓存的裁剪完之后更新进来
│   │   ├── train.json   训练的参数、状态、结果
│   │   ├── predict.json 预测的参数、状态、结果
│   │   ├── train     训练数据目录
│   │   │   ├── 1  分类1
│   │   │   ├── 7  分类7
│   │   │
│   │   ├── predict     预测数据目录
│   │   │   ├── 1  分类1
│   │   │   ├── 7  分类7
│
├── modules     存放系统默认会提供的模型文件,以及上传的模型文件
│   ├── detector  细胞定位用的模型文件
│   │   ├── deepretina_final.h5    默认mid=1的模型文件
│   │
│   ├── classifier  细胞分类用的模型文件
│   │   ├── xxxx.h5
│
├── cache     前端图片的缓存目录
│   ├── 4975136c25e8359d99ec00434dc9b96566e3e1fc260b2a96af5fa545968481b4  图片缓存文件
```

##### 文件命名约定
细胞图片名字
```
20190523.1807199.IMG002x013.JPG_1_100_0_1_x1_y1_x2_y2.png
       ^       ^          ^   ^ ^ ^   ^ ^ ^  ^  ^  ^
       |       |          |   | | |   | | |  |  |  +---- 细胞在原图的坐标y2
       |       |          |   | | |   | | |  |  +------- 细胞在原图的坐标x2
       |       |          |   | | |   | | |  +---------- 细胞在原图的坐标y1
       |       |          |   | | |   | | +------------- 细胞在原图的坐标x1
       |       |          |   | | |   | +--------------- 模型文件的id
       |       |          |   | | |   +----------------- 裁剪的方式
       |       |          |   | | +--------------------- 裁剪尺寸
       |       |          |   | +----------------------- 用灰色图片预测
       |       |          |   +------------------------- 图片后缀
       |       |          +----------------------------- 图片名
       |       +---------------------------------------- 病例
       +------------------------------------------------ 批次
```

#### 3 参数
<table class="tg">
  <tr>
    <th class="tg-0pky">任务类型</th>
    <th class="tg-0pky">参数名</th>
    <th class="tg-0pky">参数说明</th>
  </tr>
  <tr>
    <td class="tg-lboi" rowspan="5">数据处理</td>
    <td class="tg-0pky">gray</td>
    <td class="tg-0pky">默认True使用灰色，False使用彩色</td>
  </tr>
  <tr>
    <td class="tg-0pky">size</td>
    <td class="tg-0pky">切割的正方形边长，默认100</td>
  </tr>
  <tr>
    <td class="tg-0pky">type</td>
    <td class="tg-0pky">0--图片直接检测并切割出细胞 1--按照标注csv切割细胞 2--mask-rcnn检测细胞和csv交集的切割</td>
  </tr>
  <tr>
    <td class="tg-0pky">mid</td>
    <td class="tg-0pky">模型文件的id</td>
  </tr>
  <tr>
    <td class="tg-0lax">cache</td>
    <td class="tg-0lax">是否使用裁剪过的cache</td>
  </tr>
  <tr>
    <td class="tg-0pky">训练</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">预测</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
</table>


#### 4 例子
```
import time
from SDK.worker import worker
from SDK.const.const import wt

#worker 实际需要处理的任务的函数
def worker_load(wk):
    for i in range(100):
        #向服务器端报告任务进度
        wk.woker_percent(int(95 * i / 100), (100 - i) * 4)

        #do something
        time.sleep(1)

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
        print(w.datasetinfo)

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
```
