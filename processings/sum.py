#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import requests

""" 
Script to apply a simple sum to input number (called as subProcess)
"""

if __name__ == "__main__":

    # Global variables for requests
    BASE_URL = "http://127.0.0.1:5000/"
    headers = {"Content-type": "application/json"}
    
    # Get input
    # Check arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputjson", help="input json file")
    args = parser.parse_args()

    # Get elts from input json file
    JsonData = {}
    with open(args.inputjson) as f:
        JsonData = json.load(f)

    
    # Init the data after sum processings 
    dataSum = {}
    dataSum['numbers_id'] = JsonData['numbers_id'] # Select wanted numbers (after a print...)
    dataSum['numbers'] =  JsonData['numbers']
    # Empty lists
    dataSum['jobtodo_new'] = []
    dataSum['result'] = []
    
    # Do the sum
    for i in range(0,len(dataSum['numbers_id'])):
        dataSum['jobtodo_new'].append('sum_Done')
        res = dataSum['numbers'][i] + 2
        dataSum['result'].append(res)

    # Make the upate with the web service request
    req = requests.post(BASE_URL + "update_request",
                        data=json.dumps(dataSum),
                        headers=headers)

    # Check status code (must be 200 or 201)
    if req.status_code != 200 and req.status_code != 201 :
        print("status code sended by http shows a error : " + str(req.status_code))
        quit()
