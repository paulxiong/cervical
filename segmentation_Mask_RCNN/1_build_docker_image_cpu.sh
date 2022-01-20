#!/bin/bash
timestamp=$(date "+%Y%m%d%-H%-M%-S")

mv mrcnn/SDK mrcnn/SDK.bk
cp ../SDK/ mrcnn/SDK -a

docker build -f Dockerfile.cpu -t cervical:crop_mr_${timestamp} .

rm -rf mrcnn/SDK
mv mrcnn/SDK.bk mrcnn/SDK
