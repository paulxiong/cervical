# coding=utf-8
import requests, json
import time

token="token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzkyNTY0NjcsIm9yaWdfaWF0IjoxNTc2NjY0NDY3LCJ1c2VyLklkIjoxM30.SQQKpYR36Wqx5GeK8wNA8oZwNoYCwDekA8AVx3_aRxQ"

def get_datasets_info(did):
    url = "http://medical.raidcdn.cn:3000/api1/jobresult"
    headers = {"Authorization": token}
    params = {"did": did, "done": 1, "limit": 0, "skip": 0, "limit2": 0, "skip2": 0}

    response = None
    try:
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        print(e)

    fovcnt = 0
    if 200 == response.status_code:
        r = response.text.encode('utf-8')
        r = json.loads(r)
        fovcnt = r['data']['fovcnt']
    return fovcnt

def get_projects_info(p1n0=1):
    url = "http://medical.raidcdn.cn:3000/api1/listprojects"
    headers = {"Authorization": token}
    params = {"limit": 67, "skip": 0, "order": 1}

    response = None
    try:
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        print(e)

    if 200 == response.status_code:
        r = response.text.encode('utf-8')
        r = json.loads(r)
        projects = r['data']['projects']
        for p in projects:
            if p1n0 == 0:
                if p['desc'].find('p') > 0 or p['desc'].find('P') > 0:
                    continue
            elif p1n0 == 1:
                if p['desc'].find('n') > 0 or p['desc'].find('N') > 0:
                    continue
            allinfo = {"cells": {}}
            allinfo['id'], allinfo['did'], allinfo['desc'] = p['id'], p['did'], p['desc']
            for c in p['cellstype']:
                allinfo['cells'][str(c['type'])] = c['total']
            cnt50, cnt51, cnt200 = 0, 0, 0
            if '50' in allinfo['cells'].keys():
                cnt50 = allinfo['cells']['50']
            if '51' in allinfo['cells'].keys():
                cnt51 = allinfo['cells']['51']
            if '200' in allinfo['cells'].keys():
                cnt200 = allinfo['cells']['200']

            fovcnt = get_datasets_info(allinfo['did'])

            print("%s, %d, %d, %d, %d, %d, %d" % (allinfo['desc'], allinfo['id'], allinfo['did'], cnt50, cnt51, cnt200, fovcnt))

get_projects_info(1)
get_projects_info(0)
