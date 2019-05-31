FROM cellprofiler/cellprofiler:3.1.8
COPY sources.list /etc/apt/sources.list
RUN apt-get update -y && apt-get install -y  --no-install-recommends --allow-unauthenticated \
    libfreetype6 libfontconfig libgtk2.0-0 libnotify4 libgconf2-4 libnss3-1d libxss1 libasound2 xvfb x11vnc openbox git

RUN apt-get -y autoremove
RUN apt-get -y clean

RUN mkdir ~/.vnc
RUN x11vnc -storepasswd 123456 ~/.vnc/passwd

RUN mkdir -p /root/.local/share/ && \
    git clone https://github.com/CellProfiler/CellProfiler-plugins /root/plugins && \
    pip install -r /root/plugins/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && rm -rf /root/.cache/pip/* && ls -la

COPY start.sh start.sh
#CMD xvfb-run --auto-servernum --server-args="-screen 0 1280x760x24"  ./start.sh
CMD bash ./start.sh
ENTRYPOINT [""]
