FROM ubuntu:18.04
MAINTAINER ggxxde@163.com
ADD assets/sources.list /etc/apt/sources.list
RUN mkdir /data && apt-get update && \
    apt-get -y --no-install-recommends install ca-certificates curl && \
    apt-get clean
COPY release.tgz /data/release.tgz
WORKDIR /data
RUN find . && tar -xvmf release.tgz && rm -rf release.tgz && ls -lh
HEALTHCHECK --interval=60s --timeout=3s CMD curl --fail http://localhost:80/api1/ping || exit 1
EXPOSE 80
