```
一、现成环境t-sne环境使用：
 进入:http://2j592d3300.wicp.vip:8896/terminals/2
 密码：7f17dbf0c995f4ebf3d14e4767eaf923b98095cafc20802f
 进入t-sne目录： 
 cd /notebooks/hou/T_SNE.git
 运行代码：
 python3.6 tsne.py 
 如果需要更改可视化的数据打开代码对101和102行做修改，把cell_N1文件夹和cell_P文件夹改成需要测试的文件目录即可。
 代码如下：
    if __name__=="__main__":
    N_img_dataset,N_lable = read_N_directory("cell_N1") 
    P_img_dataset,P_lable = read_P_directory("cell_P2") 
```
```
二、搭建环境并运行t-sne步骤
1、环境依赖配置
  进入docker
  升级python3.5到3.6
   sudo apt-get install software-properties-common
   sudo add-apt-repository ppa:jonathonf/python-3.6 
   sudo apt-get update 
   sudo apt-get install python3.6
  让pip之类指向python3.6
   apt-get remove python3-pip
   apt-get autoremove
   apt-get install python3-pippython3.6 -m 
   pip install --upgrade pip   
 安装依赖包
   pip install opencv-python  -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
   pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
   pip install seabon -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
   如果缺少其它包再安装即可（我的环境只缺少这三个包）

2、数据准备
   准备切割和筛选好的细胞级别图片，目前代码只能完成二分类数据可视化。
   将阴性细胞和阳性细胞分别存放于两个文件夹，文件夹必须和代码在同级目录，目录结构如下：
  
   ├── tsne.py 
   ├── cell_N1
        ├── 20190523_1816688_IMG029x030.JPG_1800_1134.png
        ├── 20190523_1816696_IMG002x014.JPG_802_788.png
        ├── 20190523_1816696_IMG008x008.JPG_1634_46.png
         .
         .
        ├── 20190523_1816696_IMG008x008.JPG_1646_106.png
        ├── 20190523_1816696_IMG008x021.JPG_146_665.png
 
   ├── cell_P1── 20190523_1816527_IMG043x015.JPG_1416_374.png
        ├── 20190523_1816527_IMG043x015.JPG_1535_197.png
        ├── 20190523_1816527_IMG043x015.JPG_948_706.png
        ├── 20190523_1816527_IMG050x016.JPG_1126_960.png
         .
         .  
        ├── 20190523_1816527_IMG050x016.JPG_1134_932.png
        ├── 20190523_1816527_IMG050x016.JPG_1176_994.png

  对应的阴性细胞文件夹里可以存放多种类型的阴性细胞，阳性细胞文件夹里可以存放多种类型的阳性细胞，但是这个算法目前只完成阴性和阳性细胞的 
  二分类。            
```
```
3、t-sne可视化分类
 打开代码，修改101行和102行，把cell_N1文件夹和cell_P2文件夹改成需要测试的文件目录即可。
 代码如下：
    if __name__=="__main__":
    N_img_dataset,N_lable = read_N_directory("cell_N1") 
    P_img_dataset,P_lable = read_P_directory("cell_P2") 

  113行更改成自己要输出的图片名字： 
    plt.savefig('tsne_result.png', dpi=120)

  保存修改的代码
 运行代码：
  python3.6 tsne.py
 等待生成
 生成完成后，同级目录下查看生成的可视化分类图片。
```
