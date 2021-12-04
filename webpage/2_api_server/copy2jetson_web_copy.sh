#!/bin/bash
echo "running... copy2jetsh.sh"
scp -i ~/.ssh/jetson_rsa release.tgz bxiong@192.168.1.74:/home/bxiong/
#scp -i ~/.ssh/jetson_rsa docker-compose.yml bxiong@192.168.1.74:/home/bxiong/cervical.git/webpage/2_api_server/
ssh -i ~/.ssh/jetson_rsa bxiong@192.168.1.74 \
<<EOF
cd ~/cervical.git/webpage/2_api_server
echo "in Jetson now..."
source copy_web_to_cervical.sh

EOF
echo "exit..."

