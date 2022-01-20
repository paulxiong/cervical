docker run -d --name="cervical_mala" \
    --log-opt max-size=100m \
    -v /data/datadir:/ai \
    -e WEBURL='http://192.168.1.77:9002' \
    -e ROOTDIR='/ai/thumbor/data/loader' \
    -e PYTHONUNBUFFERED=0 \
  cervical:mala_202201139525 python3 main_SDK.py
