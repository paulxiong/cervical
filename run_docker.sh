#!/bin/bash

show_usage="./run_docker.sh {'task':image_classification_train, image_classification_predict, image_classification}"

echo "Task: $1"

docker_name=$2
function build_docker()
{
    a=`docker ps | grep "$docker_name" | wc -l`
    echo $a
    b=`docker container ls -a | grep "$docker_name" | wc -l`
    echo $b
    
    #echo $a
    if [ $a -eq 0 ];then
        if [ $b -eq 0 ];then
            docker run -d -v `pwd`:/nu_gan --name="$docker_name" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h 
            docker exec -it $docker_name bash -c "pip install tensorboardX"
        else
            docker start $docker_name 
            #docker exec -it nu_gan_test bash -c "cd /nu_gan; bash"
        fi
    fi
}

function check_env()
{
    file=`ls -lah ./experiment/data/cell_level_label | grep '^-' | wc -l`
    if [ $file -eq 0 ];then
        cell_train=`ls ~/Dataset/private_cervical/Nu_Gan/CellLevel/`
        echo "细胞级训练数据不存在，拷贝哪一批数据："
        cnt=1
        for i in $cell_train 
        do
            echo "${cnt}) ${i}"
            cnt=`expr $cnt + 1`
        done
        read -p "请输入完整目录名称(如2019-05-23):" val
        echo $vall
        while [ ! -d ~/Dataset/private_cervical/Nu_Gan/CellLevel/$val ]; do
            echo `ls ~/Dataset/private_cervical/Nu_Gan/CellLevel/$val`
            read -p "请重新输入:" val
        done
        
        mkdir -p ./experiment/data/cell_level_label
        cp ~/Dataset/private_cervical/Nu_Gan/CellLevel/$val/* ./experiment/data/cell_level_label
    fi
}


if [ -n "$1" ];then    
    check_env
    build_docker
    docker exec -it $docker_name bash -c "cd /nu_gan; python nu_gan.py --task ${1}"
else
    echo $show_usage

fi

