#!/bin/bash
timestamp=$(date "+%Y%m%d%-H%-M%-S")

mv SDK SDK.bk
cp ../../SDK/ SDK -a

docker build -f Dockerfile -t cervical:y4mala_${timestamp} .

rm -rf SDK
mv SDK.bk SDK

