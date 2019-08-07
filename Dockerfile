#FROM tensorflow/tensorflow:1.7.1-gpu-py3
FROM tensorflow/tensorflow:1.9.0-gpu
ADD HistomicsTK.tar /root/
RUN mv /etc/apt/sources.list.d/cuda.list /etc/apt/sources.list.d/cuda.list.bk && \
    mv /etc/apt/sources.list.d/nvidia-ml.list /etc/apt/sources.list.d/nvidia-ml.list.bk && \
    pip2 install 'networkx==2.2' -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && \
    cd /root/HistomicsTK &&  pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt && \
    pip2 install -e . && \
    apt-get update && apt-get -y --no-install-recommends install libsm-dev libxrender-dev python-tk language-pack-en && \
    apt-get clean && mkdir -p /data/segmentation/src/utilslib/ && \
    touch /data/segmentation/__init__.py && \
    touch /data/segmentation/src/__init__.py && \
    touch /data/segmentation/src/utilslib/__init__.py
ENV LANG "en_US.UTF-8"
WORKDIR /data
ADD segmentation/src/utilslib/webserverapi.py segmentation/src/utilslib/webserverapi.py
ADD *.py /data/
COPY utils/ /data/utils
ADD requirements.txt /data/requirements.txt
ADD torch-0.3.1-cp27-cp27mu-linux_x86_64.whl torch-0.3.1-cp27-cp27mu-linux_x86_64.whl
RUN pip2 install ./torch-0.3.1-cp27-cp27mu-linux_x86_64.whl && rm -f torch-0.3.1-cp27-cp27mu-linux_x86_64.whl && \
    pip2 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
RUN ls -alh && find /data && rm -rf /root/.nv/
