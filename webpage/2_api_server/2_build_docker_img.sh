#!/bin/bash
go build -v -o main.exe main.go
if [ ! -f main.exe ]; then
    echo "not found main.exe"
    exit 1
fi

pushd web
    npm install
    npm run build:prod
popd

rm -rf release.tgz
tar -czvmf release.tgz main.exe configs/conf.ini web/dist/
if [ ! -f release.tgz ]; then
    echo "not found release.tgz"
    exit 2
fi

rm -rf main.exe

gitid=$(git rev-parse --short HEAD)

echo "docker build -t lambdazhang/cervical:"${gitid}" ."
