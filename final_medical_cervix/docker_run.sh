#!/bin/bash
sudo docker run --rm -it --init \
  --runtime=nvidia \
  --ipc=host \
  --volume=$PWD:/cervical \
  tensorflow/tensorflow:latest-gpu-py3 sh -c "cd /cervical && ./run.sh all "
