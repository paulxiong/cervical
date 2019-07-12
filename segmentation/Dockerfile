#FROM tensorflow/tensorflow:1.7.1-gpu-py3
FROM tensorflow/tensorflow:1.7.1-py3
RUN apt-get update && apt-get install -y --no-install-recommends libsm-dev libxrender-dev git vim python3-tk && apt-get clean && mkdir /data
ADD segmentation /data
WORKDIR /data
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
RUN ls -alh
