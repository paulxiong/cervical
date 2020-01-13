# coding=utf-8
import requests, json, time, os

rooturl="http://192.168.1.107:3000"
token="token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzkyNTY0NjcsIm9yaWdfaWF0IjoxNTc2NjY0NDY3LCJ1c2VyLklkIjoxM30.SQQKpYR36Wqx5GeK8wNA8oZwNoYCwDekA8AVx3_aRxQ"

def uploadDatasets(bid, mid, filepath):
    ret = False
    if not os.path.exists(filepath) or len(bid) < 1 or len(mid) < 1:
        print("bad args %s %s %s" % (bid, mid, filepath))
        return ret
    url = rooturl + "/api1/upload"
    headers = {"Authorization": token}
    params = {"bid": bid, "mid": mid}

    files = {'file': open(filepath, 'rb')}
    response = None
    try:
        response = requests.post(url=url, files=files, data=params, headers=headers)
    except Exception as e:
        print(e)
    if 200 == response.status_code:
        json1 = response.json()
        ret = True
        if json1 is None or json1['status'] != 0:
            print("upload failed %s %s %s" % (bid, mid, filepath))
            ret = False
    return  ret

def create_dataset(bid, mid, desc):
    did = 0
    if len(bid) < 1 or len(mid) < 1 or len(desc) < 1:
        print("bad args %s %s %s" % (bid, mid, desc))
        return None

    url = rooturl + "/api1/createdataset"
    headers = {"Authorization": token}
    params = {"parameter_cache": 1, "parameter_gray": 1, "parameter_mid": 2, "parameter_size": 100, "parameter_type": 0}
    params["batchids"] = [bid]
    params["medicalids"] = [mid]
    params["desc"] = desc

    response = None
    try:
        response = requests.post(url=url, data=json.dumps(params), headers=headers)
    except Exception as e:
        print(e)

    json1 = response.json()
    if 200 == response.status_code:
        json1 = response.json()
        if json1 is None or json1['status'] != 0:
            did = 0
            print("createdataset failed status=%d" % json1['status'])
        else:
            did = json1['data']
    return did

def get_datasets_info(did):
    url = rooturl + "/api1/jobresult"
    headers = {"Authorization": token}
    params = {"did": did, "done": 1, "limit": 0, "skip": 0, "limit2": 0, "skip2": 0}

    response = None
    try:
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        print(e)

    dataset = None
    if 200 == response.status_code:
        json1 = response.json()
        if json1 is None or json1['status'] != 0:
            dataset = None
            print(json1)
        else:
            dataset = json1['data']
    return dataset

def gen_batchid_midicalid():
    batchid, midicalid = '', ''
    day1 = 86400*1000
    ts = int(time.time()*1000)
    dts = ts - int((ts % day1))

    batchid, midicalid = "b" + str(dts), "m" + str(ts)
    return batchid, midicalid

def _get_filelist(dirpath, suffix=['.jpg', '.JPG']):
    files = []
    if not os.path.isdir(dirpath):
        return files
    for j in os.listdir(dirpath):
        path2 = os.path.join(dirpath, j)
        if os.path.isdir(path2):
            continue
        ext = os.path.splitext(path2)[1]
        ext = ext.lower()
        if not ext in suffix:
            # print("skip %s" % path2)
            continue
        else:
            files.append(path2)
    return files

def create_project(did, desc):
    if did < 1 or len(desc) < 1:
        print("bad args %d %s" % (did, desc))
        return None

    url = rooturl + "/api1/createproject"
    headers = {"Authorization": token}
    params = {"celltypes": [100], "parameter_mid": 4, "parameter_resize": 100, "parameter_time": 1800, "parameter_type": 0, "type": 3}
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
    dirpath="/media/disk/tmp/dt/5#20191221"
    dirname="5#20191221"
    #想要上传的病历号写在这个里面
    mids=["1903536", "1903610", "1903615", "1903640", "1903665", "1903688", "1903694", "1903699", "1903704", "1903710", \
          "1903716", "1903721", "1903726", "1903731", "1903736", "1903741", "1903746", "1903751", "1903606", "1903611", \
          "1903616", "1903641", "1903661", "1903666", "1903679", "1903689", "1903695", "1903700", "1903705", "1903711", \
          "1903717", "1903722", "1903727", "1903732", "1903737", "1903742", "1903747", "1903752", "1903607", "1903612", \
          "1903637", "1903642", "1903662", "1903667", "1903685", "1903691", "1903696", "1903701", "1903706", "1903712", \
          "1903718", "1903723", "1903728", "1903733", "1903738", "1903743", "1903748", "1903753", "1903608", "1903613", \
          "1903638", "1903643", "1903663", "1903668", "1903686", "1903692", "1903697", "1903702", "1903707", "1903713", \
          "1903719", "1903724", "1903729", "1903734", "1903739", "1903744", "1903749", "1903754", "1903609", "1903614", \
          "1903639", "1903644", "1903664", "1903687", "1903693", "1903703", "1903708", "1903715", "1903720", "1903725", \
          "1903730", "1903740", "1903745", "1903750", "903690"]

    for m in mids:
        print("\n\n%s ======================" % m)
        imgdir=os.path.join(dirpath, m, "Images")
        if not os.path.isdir(imgdir):
            continue
        filelits = _get_filelist(imgdir)
        if len(filelits) < 1:
            continue

        print("1 uploading imgs...")
        _bid, _mid = gen_batchid_midicalid()
        uploadcnt = {'ok': 0, 'failed': 0}
        for img in filelits:
            ret = uploadDatasets(_bid, _mid, img)
            if ret is True:
                uploadcnt['ok'] = uploadcnt['ok'] + 1
            else:
                uploadcnt['failed'] = uploadcnt['failed'] + 1
        print(uploadcnt)
        print("2 uploading imgs done")

        print("3 creating dataset...")
        did = create_dataset(_bid, _mid, dirname + '+' + m)
        print("4 creating dataset done %d" % did)

        print("5 cropping dataset...")
        goterror=False
        while 1:
            ret = get_datasets_info(did)

            status=ret['status']
            if status == 3:
                goterror=True
                print("datasets error")
                break
            if status == 4:
                break
            time.sleep(5)
        print("6 cropping dataset done")
        if goterror is True:
            continue

        print("7 creating project...")
        pid = create_project(did, dirname + '+' + m)
        print("8 creating project done %d" % pid)
