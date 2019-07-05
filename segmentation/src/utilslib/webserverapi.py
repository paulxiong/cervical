# coding=utf-8
import requests, json, logging
import time
import sys, os
from uuid import uuid1

env_dist = os.environ
webhost = env_dist.get('WEBURL', 'http://9200.gpu.raidcdn.cn:9700')

debug_on = True
ml_first = True

logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True

def post2webserver(path=None, payload=None):
    if path is None or payload is None:
        return None
    print(path, payload)

    api_url = webhost + path

    try:
        response = requests.post(api_url, data=payload, timeout=4)
    except Exception as e:
        print(e)
    else:
        if 200 == response.status_code:
            response.text.encode('utf-8')
            if debug_on:
                print('post2webserver ssucceed ! ' + path)
                print(response.status_code)
                print(response.url)
                print(response.text.encode('utf-8'))
                #jobjson = json.loads(response.text)
                #code    = jobjson.get("code",  None)
                #print(code)
            return response.text.encode('utf-8')
        else:
            return None

def post_api_model(payload):
    return post2webserver('/api/model', payload)

def post_api_traing(payload):
    return post2webserver('/api/traing', payload)

def post_api_job(payload):
    global ml_first

    if ml_first:
        ml_first = False
        payload['ml_first'] = 'true'
    return post2webserver('/api/job', payload)

def get_one_job():
    """
    Tries to get the job from web server.

    :param name:
    :return: code, job_info, dataset_info, hyperparameters
    """

    payload = {}
    job = post_api_job(payload)
    if job is None:
        return None, None, None, None

    try:
        jobjson = json.loads(job.decode())
    except Exception as ex:
        print(ex)
        code = None
        return None, None, None, None
    else:
        code    = jobjson.get("code",  None)
        job     = jobjson.get("job",  None)
        study   = jobjson.get("study",  None)
        hyperparameters = jobjson.get("hyperparameters",  None)

        if code is None:
            return None, None, None, None

        code = int(code)
        if code == 3002 and job is not None and study is not None:
            if debug_on:
                print('got a trainning job')
            return code, job, study, hyperparameters 
        elif code == 3003:
            if debug_on:
                print('got a forecast job')
            return code, None, None, None
        else:
            reason = jobjson.get("reason",  None)
            if debug_on:
                print('got a unknown job: ' + str(reason))
            return None, None, None, None


#def post_prediction_result(jpg_dir, study_id, job_id):
#    instances = []
#    #upload jpg file to qiniu
#    for f in  os.listdir(jpg_dir):
#        file_path = jpg_dir + f
#        if os.path.isdir(file_path):
#            continue
#
#        nodule_chance = f.split("_")[0]
#
#        key = str(uuid1())
#        url = qiniu_upload_img(key, file_path, timeout=4)
#        if len(url) > 1:
#            #instances.append(json.dumps({'imgUrl': url, 'percent':nodule_chance}))
#            obj = {"imgUrl": url, "percent":nodule_chance}
#            instances.insert(len(instances), obj)
#
#    result = "良性"
#    percent = '0.00'
#    forecast_status = 'done'
#
#    if len(instances) > 0:
#        result = "恶性"
#
#    payload = {
#               'result': result,
#               'percent': percent,
#               'instances': json.dumps(instances),
#               'study_id': study_id,
#               'job_id': job_id,
#               'forecast_status': forecast_status
#               }
#    post2webserver(path='/api/forecast', payload=payload)
