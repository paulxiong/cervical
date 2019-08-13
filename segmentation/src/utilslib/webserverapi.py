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
        response = requests.post(api_url, json=payload, timeout=4)
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
    return post2webserver('/api1/job', payload)

def get_one_job(status, _type):
    """
    Tries to get the job from web server.

    :param name:
    :return: status, job_info
    """

    payload = {'id': 0, 'status': status, 'type': _type}
    job = post_api_job(payload)
    if job is None:
        return None, None, None

    try:
        jobjson = json.loads(job.decode())
        status = jobjson['data']['status']
        dirname = jobjson['data']['dir']
        jobid = jobjson['data']['id']
        datatype = jobjson['data']['type']
    except Exception as ex:
        print(ex)
        code = None
        return None, None, None, None
    else:
        if status is None:
            return None, None, None, None

        status = int(status)
        if status == 1 and dirname is not None:
            if debug_on:
                print('got a crop job')
            return jobid, status, dirname, datatype
        elif status == 4 and dirname is not None:
            if debug_on:
                print('got a train job')
            return jobid, status, dirname, datatype
        else:
            return None, None, None, None

def post_job_status(jobid, status):
    payload = {'id': jobid, 'status': status}
    post2webserver(path='/api1/jobresult', payload=payload)
