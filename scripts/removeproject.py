# coding=utf-8
import requests, json, time, os

rooturl="http://medical.raidcdn.cn:3000"
token="token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODU0NTI1MTIsIm9yaWdfaWF0IjoxNTgyODYwNTEyLCJ1c2VyLklkIjoyNX0.zlP-xMzgUGgZiBf-VFzvUROblV-RJvs_Sxz6QtsE-Tk"

def remove_project(pid, dropdt):
    url = rooturl + "/api1/removeproject"
    headers = {"Authorization": token}
    params = {"pid": pid, "dropdt": dropdt}

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
    projects = [2166, 2167, 2168, 2169, 2170, 2172, 2173, 2174, 2175, 2176, 2177, 2178, 2179, 2180, 2181, 2182, 2183, 2184, 2185, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2200, 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214, 2215, 2216, 2217, 2218, 2219, 2220, 2221, 2222, 2223, 2224, 2225, 2226, 2227, 2228, 2229, 2230, 2231, 2232, 2233, 2234, 2235, 2236, 2237, 2239]
    for pid in projects:
        remove_project(pid, 0)
