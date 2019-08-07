FROM tensorflow/tensorflow:1.9.0-gpu-py3
#FROM tensorflow/tensorflow:1.7.1-py3
RUN mv /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/cuda.list.bk && \
    mv /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/nvidia-ml.list.bk && \
    apt-get update && apt-get install -y --no-install-recommends libsm-dev libxrender-dev git vim python3-tk language-pack-en && \
    apt-get clean && mkdir /data
ENV LANG "en_US.UTF-8"
ADD segmentation /data
WORKDIR /data
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && find . && rm -rf /root/.nv/
