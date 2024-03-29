#!/bin/bash
#该脚本只测试过在Linux环境执行
swag init
GOOS="linux" GOARCH="arm64" go build -v -o main.exe -ldflags="-w -s" main.go
if [ ! -f main.exe ]; then
    echo "not found main.exe"
    exit 1
fi
./assets/upx main.exe

pushd web
    npm install
    npm run build:alpha
popd

rm -rf release.tgz
tar -czvmf release.tgz main.exe configs/conf.ini web/dist/ web/src/const/errCode.json
if [ ! -f release.tgz ]; then
    echo "not found release.tgz"
    exit 2
fi

rm -rf main.exe

gitid=$(git rev-parse --short HEAD)

echo "docker build -t lambdazhang/cervical:"${gitid}" -f Dockerfile.armv8 ."
