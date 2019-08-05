FROM tensorflow/tensorflow:1.9.0-gpu-py3
#FROM tensorflow/tensorflow:1.7.1-py3
RUN apt-get update && apt-get install -y --no-install-recommends libsm-dev libxrender-dev git vim python3-tk language-pack-en && apt-get clean && mkdir /data
ENV LANG "en_US.UTF-8"
ADD segmentation /data
WORKDIR /data
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
RUN ls -alh
