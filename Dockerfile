#FROM tensorflow/tensorflow:1.7.1-gpu-py3
FROM tensorflow/tensorflow:1.7.0
ADD HistomicsTK.tar /root/
RUN pip2 install 'networkx==2.2' -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && \
    cd /root/HistomicsTK &&  pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt && \
    pip2 install -e . && \
    apt-get update && apt-get -y --no-install-recommends install libsm-dev libxrender-dev python-tk && apt-get clean && mkdir /data
WORKDIR /data
ADD nu_gan.py /data/nu_gan.py
COPY utils/ /data/utils
ADD requirements.txt /data/requirements.txt
RUN pip2 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
RUN ls -alh && find /data
