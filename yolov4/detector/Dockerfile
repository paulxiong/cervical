FROM tensorflow/tensorflow:1.4.0-gpu-py3
ENV DEBIAN_FRONTEND "noninteractive"
RUN mv /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/cuda.list.bk && \
    mv /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/nvidia-ml.list.bk && \
    apt-get update && apt-get -y --no-install-recommends install libsm-dev libxrender-dev language-pack-en openssh-server libopencv-dev && \
    apt-get clean

ENV LANG "en_US.UTF-8"
ENV PYTHONUNBUFFERED "0"

WORKDIR /notebooks/data
ADD requirements.txt /notebooks/data/requirements.txt
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && \
    rm -rf /root/.nv/ && rm -rf requirements.txt && ls -alh
ADD libdarknet.so libdarknet.so
ADD main_SDK.py main_SDK.py
ADD SDK SDK
ADD names-data names-data
ADD cells_detect_crop.py cells_detect_crop.py
ADD kernelpredict.py kernelpredict.py
