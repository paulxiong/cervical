# coding=utf-8
import requests, json, os

class api():
    def __init__(self, apihost, debug=False):
        self.apihost = apihost
        self.debug = debug

    def post2webserver(self, path=None, payload=None):
        if path is None or payload is None:
            return None
        if self.debug:
            print(path, payload)
        api_url = self.apihost + path
        try:
            response = requests.post(api_url, json=payload, timeout=4)
        except Exception as e:
            print(e)
        else:
            if 200 == response.status_code:
                response.text.encode('utf-8')
                if self.debug:
                    print('post2webserver ssucceed ! ' + path)
                    print(response.status_code)
                    print(response.url)
                    print(response.text.encode('utf-8'))
                return response.text.encode('utf-8')
            else:
                return None

    def post_api_job(self, payload):
        return self.post2webserver('/api1/job', payload)

    def get_one_job(self, status, _type):
        payload = {'id': 0, 'status': status, 'type': _type}
        job = self.post_api_job(payload)
        if job is None:
            return None, None, None
        try:
            jobjson = json.loads(job.decode())
            status = jobjson['data']['status']
            dirname = jobjson['data']['dir']
            jobid = jobjson['data']['id']
        except Exception as ex:
            print(ex)
            code = None
            return None, None, None
        else:
            if status is None:
                return None, None, None

            status = int(status)
            return jobid, status, dirname

    def post_job_status(self, jobid, status, percent):
        payload = {'id': jobid, 'status': status, 'percent': percent}
        post2webserver(path='/api1/jobresult', payload=payload)
