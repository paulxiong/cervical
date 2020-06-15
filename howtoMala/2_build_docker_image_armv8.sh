#!/bin/bash
timestamp=$(date "+%Y%m%d%-H%-M%-S")

mv SDK SDK.bk
cp ../SDK/ SDK -a

mkdir -p tmp
pushd tmp
    if [ ! -e OpenCV-3.4.3-aarch64-dev.deb ]; then
        wget https://github.com/lambda-zhang/OpenCV_Xavier_whl/releases/download/3.4.3/OpenCV-3.4.3-aarch64-dev.deb
    fi
    if [ ! -e OpenCV-3.4.3-aarch64-libs.deb ]; then
        wget https://github.com/lambda-zhang/OpenCV_Xavier_whl/releases/download/3.4.3/OpenCV-3.4.3-aarch64-libs.deb
    fi
    if [ ! -e OpenCV-3.4.3-aarch64-licenses.deb ]; then
        wget https://github.com/lambda-zhang/OpenCV_Xavier_whl/releases/download/3.4.3/OpenCV-3.4.3-aarch64-licenses.deb
    fi
    if [ ! -e opencv_python-3.4.3-cp36-cp36m-linux_aarch64.whl ]; then
        wget https://github.com/lambda-zhang/OpenCV_Xavier_whl/releases/download/3.4.3/opencv_python-3.4.3-cp36-cp36m-linux_aarch64.whl
    fi
popd

docker build -f Dockerfile.armv8  -t cervical:mala_${timestamp} .

rm -rf SDK
mv SDK.bk SDK

