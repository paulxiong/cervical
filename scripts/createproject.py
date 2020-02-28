# coding=utf-8
import requests, json, time, os

mid = 24
rooturl="http://medical.raidcdn.cn:3000"
token="token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODU0NTI1MTIsIm9yaWdfaWF0IjoxNTgyODYwNTEyLCJ1c2VyLklkIjoyNX0.zlP-xMzgUGgZiBf-VFzvUROblV-RJvs_Sxz6QtsE-Tk"

def create_project(did, desc, _mid):
    if did < 1 or len(desc) < 1:
        print("bad args %d %s" % (did, desc))
        return None

    url = rooturl + "/api1/createproject"
    headers = {"Authorization": token}
    params = {"celltypes": [100], "parameter_mid": _mid, "parameter_resize": 100, "parameter_time": 1800, "parameter_type": 0, "type": 3}
    params["desc"] = desc
    params["did"] = did

    response = None
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
    except Exception as e:
        print(e)

    pid = 0
    if 200 == response.status_code:
        json1 = response.json()
        if json1 is None or json1['status'] != 0:
            pid = 0
            print("createproject failed status=%d" % json1['status'])
        else:
            pid = json1['data']
    return pid

if __name__ == "__main__":
    datasets = {
        "1329": "35#20191212+1906676",
        "1336": "35#20191212+1906677+ASC-H",
        "1359": "35#20191212+1906729",
        "1363": "35#20191212+1906672+ASC-H",
        "1365": "35#20191212+1906711+低",
        "1377": "32#20191217+1906195",
        "1385": "32#20191217+1906328",
        "1387": "35#20191212+1906735",
        "1395": "32#20191217+1906330",
        "1402": "32#20191217+1906274+低HAV",
        "1409": "32#20191217+1906374+",
        "1419": "32#20191217+1906284",
        "1421": "32#20191217+1906376",
        "1424": "32#20191217+1906285",
        "1426": "32#20191217+1906337",
        "1431": "32#20191217+1906290低+HAV",
        "1432": "32#20191217+1906378",
        "1433": "32#20191217+1906338",
        "1437": "32#20191217+1906379",
        "1439": "32#20191217+1906403",
        "1442": "32#20191217+1906340+",
        "1448": "32#20191217+1906407",
        "1450": "32#20191217+1906341+A",
        "1454": "32#20191217+1906352",
        "1456": "32#20191217+1906342+低HAV",
        "1461": "32#20191217+1906363",
        "1463": "32#20191217+1906343",
        "1471": "32#20191217+1906355+A",
        "1474": "32#20191217+1906411",
        "1480": "32#20191217+1906412",
        "1494": "32#20191217+1906418",
        "1518": "32#20191217+1906421",
        "1519": "34#20191220+1906530",
        "1521": "34#20191220+1906559",
        "1522": "34#20191220+1906569",
        "1528": "34#20191220+1906560",
        "1532": "34#20191220+1906550+低",
        "1533": "32#20191217+1906424",
        "1534": "34#20191220+1906532",
        "1549": "34#20191220+1906536+A"
    }

    for did in datasets.keys():
        desc = datasets[did]
        pid = create_project(int(did), desc, mid)
        if pid < 1:
            print("create_project failed")
            exit()
        print("created %d %s with dataset %d" % (pid, desc, int(did)))
        time.sleep(1)
