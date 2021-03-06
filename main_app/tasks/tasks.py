#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Define the Celery Tasks with two kinds of tasks :
_ Async/Events tasks called by the views with delay function
_ Periodic/CRON tasks called by celery beat 
"""

from main_app.app import celery_app
from main_app.extensions import db
from main_app.models.models import Request
from main_app.models.models import Numbers

import random
import os
from pathlib import Path
import json
import pickle
import subprocess

celery = celery_app

################ Events tasks (with delay and called by views) ###########################

@celery.task()
def handle_number_requests(request_id, number_list, jobtodo_list):

    response = "OK"
    # Put the request into our DB : into request and number tables
    try :

        # First into request table
        my_request = Request(request_id=request_id, number_list=pickle.dumps(number_list),
                             jobToDo_list=pickle.dumps(jobtodo_list))
        db.session.add(my_request)
        
        # Second into number table
        # Loop on number_list and jobtodo_list to store one by one number into number table
        for i in range(0, len(number_list)):
            my_number = Numbers(numbers=number_list[i], jobToDo=jobtodo_list[i],
                                request_id=request_id)
            db.session.add(my_number)

        # Save chgts into our DB
        db.session.commit()
        
    except Exception as exc :
        # Adapt response if exception (usually if rid is already into request table)
        response = "Error during DB transaction : Please Check the request"
        
    return response



@celery.task()
def update_number_requests(Ntable_id, N_list, JTD_list, res_list):

    # List to store request_id for each number
    rId_list = []

    # General Query
    query = Numbers.query.filter(Numbers.id.in_(Ntable_id)).all()
    
    # Update first, Numbers Table and store request id
    for i in range(0, len(Ntable_id)):
        # Query on id
        #my_number = Numbers.query.filter_by(id=Ntable_id[i]).first()
        my_number = query[i] 
        # Update my number
        my_number.jobToDo = JTD_list[i]
        my_number.result_numbers = res_list[i]

        # Store rid for current number
        rId_list.append(my_number.request_id)

    # Udpate then, Request_Table
    # Get unique rid into our list
    rid_unique = set(rId_list)

    # Loop on each unique rid
    for rid in rid_unique:
        # Query on request_id
        my_request = Request.query.filter_by(request_id=rid).first()
        
        # Get all indexes with the current rid into rId_list
        indexes = [n for n,x in enumerate(rId_list) if x==rid]

        # Get number_list and jobtodo_list form current request
        rNumberList = pickle.loads(my_request.number_list)
        new_JobToDo = pickle.loads(my_request.jobToDo_list)
        

        # Loop on indexes
        for ind in indexes:
            try :
                # Udpate the right "job to do" with the number index
                indB = rNumberList.index(N_list[ind])
                new_JobToDo[indB] = JTD_list[ind]
        
            except ValueError:
                print("number is not inside the list => no update")

        my_request.jobToDo_list = pickle.dumps(new_JobToDo)

    db.session.commit()

################ Periodic tasks/CRON (called by celery beat) ###########################    

# bash commands
def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

# python scripts
def python_script(script, inputArg):
    subprocess.Popen(['python', script, inputArg])
 
#### Processings : with sum and mul operations ####
# Sum
@celery.task(bind=True)
def sum_task(self):

    # Get current task id
    currentTaskId = self.request.id

    # Select into Numbers table, number with sum to do
    numbers_to_sum = Numbers.query.filter_by(jobToDo="sum").all()

    print(len(numbers_to_sum))

    # Check number to sum (must be > 0)
    if len(numbers_to_sum) > 0:
        # Write numbers into a file
        inputJson = {}
        inputJson['numbers_id'] = []
        inputJson['numbers'] = []

        for i in range(0,len(numbers_to_sum)):
            # Extract id and numbers information
            inputJson['numbers_id'].append(numbers_to_sum[i].id)
            inputJson['numbers'].append(numbers_to_sum[i].numbers)

            # Update jobToDo with Doing
            numbers_to_sum[i].jobToDo = "sum_Doing"

        # Commit changes into our DB
        db.session.commit()
        
        # Write the json file
        JSON_PATH = os.path.join(Path(__file__).parent.parent.parent, 'processings/input_files/')
        JSON_NAME = os.path.join(JSON_PATH, currentTaskId + '.json')
        print(JSON_NAME)


        with open(JSON_NAME, 'w') as f:
            json.dump(inputJson, f)

        # Launch sum processing with a SubProcess
        SCRIPT_PATH = os.path.join(Path(__file__).parent.parent.parent, 'processings/sum.py')
        python_script(SCRIPT_PATH, JSON_NAME)

        print('Hi! from sum_task')

# Mul
@celery.task(bind=True)
def mul_task(self):

    # Get current task id
    currentTaskId = self.request.id

    # Select into Numbers table, number with mul to do
    numbers_to_mul = Numbers.query.filter_by(jobToDo="mul").all()
    
    print(len(numbers_to_mul))

    # Check number to mul (must be > 0)
    if len(numbers_to_mul) > 0:
        # Write numbers into a file
        inputJson = {}
        inputJson['numbers_id'] = []
        inputJson['numbers'] = []

        for i in range(0,len(numbers_to_mul)):
            # Extract id and numbers information
            inputJson['numbers_id'].append(numbers_to_mul[i].id)
            inputJson['numbers'].append(numbers_to_mul[i].numbers)

            # Update jobToDo with Doing
            numbers_to_mul[i].jobToDo = "mul_Doing"

        # Commit changes into our DB
        db.session.commit()
        
        # Write the json file
        JSON_PATH = os.path.join(Path(__file__).parent.parent.parent, 'processings/input_files/')
        JSON_NAME = os.path.join(JSON_PATH, currentTaskId + '.json')
        print(JSON_NAME)


        with open(JSON_NAME, 'w') as f:
            json.dump(inputJson, f)

        # Launch mul processing with a SubProcess
        SCRIPT_PATH = os.path.join(Path(__file__).parent.parent.parent, 'processings/mul.py')
        python_script(SCRIPT_PATH, JSON_NAME)

        print('Hi! from mul_task')
