#FROM tensorflow/tensorflow:1.13.2-gpu-py3
FROM tensorflow/tensorflow:1.10.0-gpu-py3
ENV DEBIAN_FRONTEND "noninteractive"
RUN mv /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/cuda.list.bk && \
    mv /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/nvidia-ml.list.bk && \
    mv /etc/apt/sources.list.d/nvinfer-runtime-trt-5.0.2-ga-cuda10.0.list /etc/apt/sources.list.d/nvinfer-runtime-trt-5.0.2-ga-cuda10.0.list.bk && \
    apt-get update && apt-get -y --no-install-recommends install libsm-dev libxrender-dev python-tk language-pack-en openssh-server && \
    apt-get clean && mkdir -p /tf/data && \
    sed -i 's/^PermitRootLogin/#PermitRootLogin/' /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "root:5F392afB7f76170d" | chpasswd && mkdir -p /var/run/sshd

ADD assets/run_jupyter.sh /run_jupyter.sh

ENV LANG "en_US.UTF-8"
ENV PYTHONUNBUFFERED "0"
WORKDIR /tf/data
ADD requirements.txt /tf/data/requirements.txt
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && \
    rm -rf /root/.nv/ && rm -rf requirements.txt && ls -alh
