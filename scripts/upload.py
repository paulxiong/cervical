# coding=utf-8
import requests, json, time, os

rooturl="http://medical.raidcdn.cn:3000"
token="token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODg0ODQ3MzksIm9yaWdfaWF0IjoxNTg1ODkyNzM5LCJ1c2VyLklkIjoxM30.6L57Qn1oS3pv5j7rjq0WULgYltax7A6qwDN9mT0aTUE"
modelID=64

def uploadDatasets(bid, mid, mdir, filepath):
    ret = False
    if not os.path.exists(filepath) or len(bid) < 1 or len(mid) < 1:
        print("bad args %s %s %s" % (bid, mid, filepath))
        return ret
    url = rooturl + "/api1/uploaddir"
    headers = {"Authorization": token}
    params = {"bid": bid, "mid": mid, "relativePath": filepath, "dir": mdir}

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
    params = {"parameter_cache": 1, "parameter_gray": 1, "parameter_mid": modelID, "parameter_size": 100, "parameter_type": 0}
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
    batchid, midicalid = time.strftime("%Y%m%d", time.localtime()), time.strftime("%Y%m%d%H%M%S", time.localtime())
    return batchid, midicalid

def _get_filelist(dirpath):
    uploadlists = []
    for i in os.listdir(dirpath):
        path1 = os.path.join(dirpath, i)
        if os.path.isfile(path1):
            uploadlists.append({'relativePath': path1})
            continue
        for j in os.listdir(path1):
            path2 = os.path.join(path1, j)
            if os.path.isfile(path2):
                uploadlists.append({'relativePath': path2})
    return uploadlists

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
    dirpath="/data/tmp"
    dirname="tmp"
    #想要上传的病历号写在这个里面
    mids=["1803595"]

    for m in mids:
        print("\n\n%s ======================" % m)
        medicaldir=os.path.join(dirpath, m)
        if not os.path.isdir(medicaldir):
            continue
        filelits = _get_filelist(medicaldir)
        if len(filelits) < 1:
            continue

        print("1 uploading imgs...")
        _bid, _mid = gen_batchid_midicalid()
        uploadcnt = {'ok': 0, 'failed': 0}
        for _file in filelits:
            ret = uploadDatasets(_bid, _mid, medicaldir, _file['relativePath'])
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
        continue

        print("7 creating project...")
        pid = create_project(did, dirname + '+' + m)
        print("8 creating project done %d" % pid)
