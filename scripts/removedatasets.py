# coding=utf-8
import requests, json, time, os

rooturl="http://medical.raidcdn.cn:3000"
token="token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODU0NTI1MTIsIm9yaWdfaWF0IjoxNTgyODYwNTEyLCJ1c2VyLklkIjoyNX0.zlP-xMzgUGgZiBf-VFzvUROblV-RJvs_Sxz6QtsE-Tk"

def remove_dataset(did):
    url = rooturl + "/api1/removedataset"
    headers = {"Authorization": token}
    params = {"did": did}

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


if __name__ == "__main__":
    datasets = [1512,1513,1514,1515,1516,1517,1900,1901,1902,1903,1904,1905,1906,1907,197,1974,1975,1976,1977,198,1999,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,205,2058,2059,2060,2061,2062,2063,2064,2065,2066,2067,2068,2069,207,2070,210,213,214,216,217,218,219,221,222,223,224,225,228,229,230,231,232,237,238,239,240,241,242,243,244,245,246,247,248,250,251,252,253,254,256,257,259,260,262,263,265,266,267,268,269,271,272,273,274,276,277,278,279,282,283,312]
    for did in datasets:
        remove_dataset(did)
