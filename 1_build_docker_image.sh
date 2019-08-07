#!/bin/bash
if [ ! -f HistomicsTK.tar ]; then
    echo "not found HistomicsTK.tar !!!"
    exit
fi
if [ ! -f torch-0.3.1-cp27-cp27mu-linux_x86_64.whl ]; then
    echo "not found  torch-0.3.1-cp27-cp27mu-linux_x86_64.whl !!!"
    exit
fi

docker build -f Dockerfile -t cervical:gan_20190807 .
