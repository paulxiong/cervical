docker run -d --name="cervical_crop" \
    --log-opt max-size=100m \
    -v /data/datadir:/ai \
    -e WEBURL='http://192.168.1.77:9002' \
    -e ROOTDIR='/ai/thumbor/data/loader' \
    -e PYTHONUNBUFFERED=0 \
  cervical:crop_mr_2022011383723 python3 main_SDK.py
