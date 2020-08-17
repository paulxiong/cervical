## 部署
```
docker run -d --name ddns \
    --restart=always \
    -v /data/km/ddns/kmxd_settings.json:/data/settings.json \
    lambdazhang/cervical-ddns:1cd0274b sh -c 'pwd && ls -la && ./main.exe'
```
