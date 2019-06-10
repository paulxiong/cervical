#!/bin/bash
show_usage='./copy_fov.sh P/N'


function copy_pos()
{
    if [ ! -d '../experiment/data/original/' ];then
        echo "不存在../experiment/data/original/， 创建目录..."
        mkdir -p ../experiment/data/original/
    fi
    
    if [ ! -d '../experiment/data/segmented/' ];then
        echo "不存在../experiment/data/segmented/， 创建目录..."
        mkdir -p ../experiment/data/segmented/
    fi
    
    if [ -d '../experiment/data/original/positive_test_images' ];then
        echo "存在../experiment/data/original/positive_test_images， 删除..."
        rm -rf ../experiment/data/original/positive_test_images
    fi
    
    if [ -d '../experiment/data/segmented/positive_test_npy' ];then
        echo "存在../experiment/data/segmented/positive_test_npy， 删除..."
        rm -rf ../experiment/data/segmented/positive_test_npy
    fi
    
    echo "拷贝异常FOV"
    cp -rf ./datasets/classify/data/original/images ../experiment/data/original/positive_test_images   
    cp -rf ./datasets/classify/data/segmented/npy ../experiment/data/segmented/positive_test_npy  
    echo "拷贝完成"
}

function copy_neg()
{
    if [ ! -d '../experiment/data/original/' ];then
        echo "不存在../experiment/data/original/， 创建目录..."
        mkdir -p ../experiment/data/original/
    fi
    
    if [ ! -d '../experiment/data/segmented/' ];then
        echo "不存在../experiment/data/segmented/， 创建目录..."
        mkdir -p ../experiment/data/segmented/
    fi
    
    if [ -d '../experiment/data/original/negative_test_images' ];then
        echo "存在../experiment/data/original/negative_test_images， 删除..."
        rm -rf ../experiment/data/original/negative_test_images
    fi
    
    if [ -d '../experiment/data/segmented/negative_test_npy' ];then
        echo "存在../experiment/data/segmented/negative_test_npy， 删除..."
        rm -rf ../experiment/data/segmented/negative_test_npy
    fi
    
    echo "拷贝正常FOV"
    cp -rf ./datasets/classify/data/original/images ../experiment/data/original/negative_test_images   
    cp -rf ./datasets/classify/data/segmented/npy ../experiment/data/segmented/negative_test_npy  
    echo "拷贝完成"
}

function copy_fov()
{
    if [ ! -d "../experiment/data" ];then
        echo "不存在../experiment/data， 创建..."
        mkdir -p ../experiment/data
    fi

    if [ -d "../experiment/data/original" ];then
        echo "../experiment/data/original已经存在，删除文件夹..."
        rm -rf ../experiment/data/original
    fi
    
    if [ -d "../experiment/data/segmented" ];then
        echo "../experiment/data/segmented已经存在，删除文件夹..."
        rm -rf ../experiment/data/segmented
    fi
    
    if [ -d "./datasets/classify/data" ];then
        echo "拷贝FOV数据..."
        cp -rf ./datasets/classify/data/original ../experiment/data/original   
        cp -rf ./datasets/classify/data/segmented ../experiment/data/segmented  
        echo "拷贝完成"
    fi
}

annot_flag=`ls -l ./datasets/classify/annot_out | grep '^-' | wc -l`
traindata_flag=`ls -l ./datasets/classify/train_datasets/default/npy | grep '^-' | wc -l`
pdata_flag=`ls -l ./datasets/classify/data/original/positive_test_images | grep '^-' | wc -l`
ndata_flag=`ls -l ./datasets/classify/data/original/negative_test_images | grep '^-' | wc -l`


if [ $annot_flag -gt 0 ] && [ $traindata_flag -gt 0];then
    echo "检测到自动标注与训练数据集，执行第一种情况..."
    copy_fov
elif [ $pdata_flag -gt 0 ] && [ $ndata_flag -gt 0 ];then
    echo "检测到已分类测试数据，执行第三种情况..."
    copy_fov
else
    echo "没有检测到自动标注与训练数据集，执行第二种情况..."
    
    if [ -n "$1" ]; then
        case "$1" in
            P)copy_pos;;
            N)copy_neg;;
            
            *) echo ${show_usage}

        esac

    fi
fi



