#!/bin/bash
timestamp=$(date "+%Y%m%d%-H%-M%-S")

docker build -f Dockerfile.cpu -t cervical:crop_mr_${timestamp} .
