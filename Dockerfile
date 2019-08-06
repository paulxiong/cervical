#FROM tensorflow/tensorflow:1.7.1-gpu-py3
FROM tensorflow/tensorflow:1.9.0-gpu
ADD HistomicsTK.tar /root/
RUN pip2 install 'networkx==2.2' -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir && \
    cd /root/HistomicsTK &&  pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt && \
    pip2 install -e . && \
    apt-get update && apt-get -y --no-install-recommends install libsm-dev libxrender-dev python-tk language-pack-en && \
    apt-get clean && mkdir /data
ENV LANG "en_US.UTF-8"
WORKDIR /data
ADD nu_gan.py /data/nu_gan.py
COPY utils/ /data/utils
ADD requirements.txt /data/requirements.txt
ADD torch-0.3.1-cp27-cp27mu-linux_x86_64.whl torch-0.3.1-cp27-cp27mu-linux_x86_64.whl
RUN pip2 install ./torch-0.3.1-cp27-cp27mu-linux_x86_64.whl && rm -f torch-0.3.1-cp27-cp27mu-linux_x86_64.whl && \
    pip2 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
RUN ls -alh && find /data
