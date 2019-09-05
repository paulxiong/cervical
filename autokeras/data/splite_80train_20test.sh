#!/bin/bash

rm -rf train test

#遍历当前目录
for dir in `find . -maxdepth 1 -type d`
do
    mkdir train test -p
    #跳过.目录
    if [ ${#dir} -lt 3 ]; then
        echo "skip "${dir}
        continue
    fi

    #当前分类的图片总数
    total=$(find ${dir} -maxdepth 1 -type f | wc -l)
    if [ ${total} -lt 2 ]; then
        echo "not enough datasets, "${dir}
    fi
    train_num=$[$total*80/100]
    cnt=0

    echo ${dir}'  total='${total}' train='${train_num}
    for img in `find ${dir} -maxdepth 1 -type f`
    do
      mkdir -p "train/"${dir}
      mkdir -p "test/"${dir}
      if [ ${cnt} -lt ${train_num} ];then
          cp -v ${img} "train/"${dir}
      else
          cp -v ${img} "test/"${dir}
      fi
      cnt=$[$cnt+1]
    done
    echo ""
done
