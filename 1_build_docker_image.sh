#!/bin/bash
if [ ! -f HistomicsTK.tar ]; then
    echo "not found HistomicsTK.tar !!!"
    exit
fi
if [ ! -f torch-0.3.1-cp27-cp27mu-linux_x86_64.whl ]; then
    echo "not found  torch-0.3.1-cp27-cp27mu-linux_x86_64.whl !!!"
    exit
fi

timestamp=$(date "+%Y%m%d%-H%-M%-S")

docker build -f Dockerfile -t cervical:gan_${timestamp} .
