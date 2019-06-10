#!/bin/bash

show_usage="./run_docker.sh ${'task':image_classification_train, image_classification_predict, image_classification}"

echo "Task: $1"

docker_name=$2
function build_docker()
{
    a=`docker ps | grep "$docker_name" | wc -l`
    echo $a
    b=`docker container ls -a | grep "$docker_name" | wc -l`
    echo $b
    
    #echo $a
    if [ ! $a -eq 0 ];then
        if [ $b -eq 0 ];then
            docker run -d -v `pwd`:/nu_gan --name="$docker_name" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h 
            docker exec -it $docker_name bash -c "pip install tensorboardX"
        else
            docker start $docker_name 
            #docker exec -it nu_gan_test bash -c "cd /nu_gan; bash"
        fi
    fi
}


if [ -n "$1" ];then    
    build_docker
    docker exec -it $docker_name bash -c "cd /nu_gan; python nu_gan.py --task ${1}"
else
    echo $show_usage

fi

