#!/bin/bash
sudo docker run --rm -it --init \
  --runtime=nvidia \
  --ipc=host \
  --volume=$PWD:/cervical_detection \
  tensorflow/tensorflow:latest-gpu-py3 sh -c "cd /cervical_detection/src/CLASSIFY/inceptionV3_final_1 && python3 final_train.py"
