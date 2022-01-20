#!/bin/bash
tar -czvmf release.tgz main.exe configs/conf.ini web/dist/ web/src/const/errCode.json
cp release.tgz /data
pushd /data
tar -zxvf release.tgz
popd 
