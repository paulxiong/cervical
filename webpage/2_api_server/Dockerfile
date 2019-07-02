FROM ubuntu:18.04
MAINTAINER ggxxde@163.com
RUN mkdir /data
COPY release.tgz /data/release.tgz
WORKDIR /data
RUN find . && tar -xvmf release.tgz && rm -rf release.tgz && ls -lh
EXPOSE 80
