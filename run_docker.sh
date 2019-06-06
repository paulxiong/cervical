#!/bin/bash

show_usage="./run_docker.sh {docker_name}"

echo $1

if [ -n "$1" ];then

    a=`docker ps | grep ${1} | wc -l`
    #echo $a
    if [ $a -gt 0 ];then
        docker exec -it $1 bash -c "cd /nu_gan; bash"
    else
        docker run -d -v `pwd`:/nu_gan --name="$1" --runtime=nvidia tensorflow/tensorflow:1.7.0-gpu-nu_gan sleep 100h 
        docker exec -it $1 bash -c "pip install tensorboardX;cd /nu_gan; bash"
    fi

else
    echo $show_usage

fi

