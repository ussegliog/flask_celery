#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import argparse
import json
import time

""" 
Script to simulate user requests
One argument request_id
"""

if __name__ == "__main__":

    # Global variables for requests
    BASE_URL = "http://127.0.0.1:5000/"
    headers = {"Content-type": "application/json"}
    
    ###### Get the only argument : request id ######
    # Check arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("rid", help="input request id")
    args = parser.parse_args()

       
    #### 1): request POST on http://127.0.0.1:5000/number_request #### 
    dataRequest = {}
    dataRequest["rid"] = args.rid
    dataRequest["numbers"] =  [51, 52, 53]
    dataRequest["jobtodo"]=  ["plus", "mul", "plus"]
    
    req = requests.post(BASE_URL + "number_request",
                        data=json.dumps(dataRequest),
                        headers=headers)

    # Check status code (must be 200 or 201)
    if req.status_code != 200 and req.status_code != 201 :
        print("status code sended by http shows a error : " + str(req.status_code))
        quit()
        
    # Get task Id
    taskIDJson = json.loads(req.text)
    
    #### 2): Wait for SUCCESS or FAILURE or REVOKED and Get Status + Response for previous task ####
    # Get status/response
    req = requests.get(BASE_URL + "check_request",
                        data=json.dumps(taskIDJson),
                        headers=headers)

    taskResponseJson = json.loads(req.text)
    status = json.loads(req.text)['status'] 
    
    while (status != "SUCCESS" and status != "FAILURE" and status != "REVOKED"):

        # Sleep 2s
        time.sleep(2)

        # Recheck the status after 2s
        req = requests.get(BASE_URL + "check_request",
                           data=json.dumps(taskIDJson),
                           headers=headers)
        
        taskResponseJson = json.loads(req.text)
        status = json.loads(req.text)['status']

        
    # Check response    
    response = json.loads(req.text)['response']
    if response != "OK" :
        print("number_request is not OK : " + response)

        
    #### 3): Re Get the request with the request id ####
    dataReRequest = {}
    dataReRequest["rid"] = args.rid
    req = requests.get(BASE_URL + "number_request",
                        data=json.dumps(dataReRequest),
                        headers=headers)
    
    # Check status code (must be 200 or 201)
    if req.status_code != 200 and req.status_code != 201 :
        print("status code sended by http shows a error : " + str(req.status_code))
        quit()

    print("At the end : " + req.text)

    #### 4): Update the request  ####
    # Try a update : with number id
    dataUpdate = {}
    dataUpdate['numbers_id'] = [13, 14, 18] # Select wanted numbers (after a print...)
    dataUpdate['numbers'] =  [51, 52, 53]
    dataUpdate['jobtodo_new']=  ["plus_Done", "mul_Done", "plus_Done"]
    dataUpdate['result'] =  [53, 104, 55]

    req = requests.post(BASE_URL + "update_request",
                        data=json.dumps(dataUpdate),
                        headers=headers)

    # Check status code (must be 200 or 201)
    if req.status_code != 200 and req.status_code != 201 :
        print("status code sended by http shows a error : " + str(req.status_code))
        quit()
