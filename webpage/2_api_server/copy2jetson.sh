#!/bin/bash
echo "running... copy2jetsh.sh"
scp release.tgz bxiong@192.168.1.74:/home/bxiong/
ssh -i ~/.ssh/2Jetson.rsa bxiong@192.168.1.74 \
<<EOF
cd ~/cervical.git/webpage/2_api_server
echo "in Jetson now..."
source run_build_cervical.sh

EOF
echo "exit..."

