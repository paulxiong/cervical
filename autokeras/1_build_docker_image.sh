#!/bin/bash
timestamp=$(date "+%Y%m%d%-H%-M%-S")

docker build -f Dockerfile -t cervical:autokeras_${timestamp} .
