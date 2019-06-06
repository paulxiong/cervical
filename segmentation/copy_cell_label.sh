#!/bin/bash
if [ ! -d "../experiment/data/cell_level_label" ];then
echo "../experiment/data/cell_level_label不存在，创建文件夹..."
mkdir -p ../experiment/data/cell_level_label
else
echo "../experiment/data/cell_level_label已经存在，删除文件..."
rm -r ../experiment/data/cell_level_label
echo "删除完成"
fi

echo "拷贝cell_level_label"
if [ -d "./datasets/classify/train_datasets/default/npy"];then
cp -r ./datasets/classify/train_datasets/default/npy ../experiment/data/cell_level_label  
echo "拷贝完成"
else
echo "cell_level_label数据不存在，请检查..."
fi