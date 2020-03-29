#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Define all available views with our Flask Application
"""

from flask import current_app as app
from flask import (Blueprint,
                   render_template,
                   request,
                   jsonify)
from celery.result import AsyncResult


from main_app.extensions import db
from main_app.models.models import Request
from main_app.models.models import Numbers

import pickle

page = Blueprint('pages', __name__, template_folder='templates')



@page.route("/")
def index():
    """
    Index / Main page
    :return: html
    """
    from main_app.tasks.tasks import my_task
    return "Pouet \n"


@page.route("/execute_task", methods=['POST'])
def _execute_task():
    """
    Invoke this function from an Ajax Call
    :return: json
    """  
    from main_app.tasks.tasks import my_task

    if request.method == 'POST':
        # Invoke celery task
        task = my_task.delay()

    return jsonify({'taskID': task.id}), 201

@page.route("/number_request", methods=['POST', 'GET'])
def number_request():
    """
    Handle request and main transactions into the request table of the DB
    """  
    from main_app.tasks.tasks import handle_number_requests

    if request.method == 'POST':
        request_id = request.json['rid'] # int
        numbers_intoRequest = request.json['numbers'] # list of numbers
        jobToDo_intoRequest = request.json['jobtodo'] # list of string
        
        # Invoke celery task to do transaction into the DB
        task = handle_number_requests.delay(request_id=request_id,
                                            number_list=numbers_intoRequest,
                                            jobtodo_list=jobToDo_intoRequest)

        # Return taskId
        return jsonify({'taskID': task.id}) , 201

    if request.method == 'GET':
        request_id = request.json['rid'] # int

        # Need to be sync => directly into our views and not inside a celery task
        # Query into request table thanks to request_id
        required_request = Request.query.filter_by(request_id=request_id).first_or_404()

        # Transform elt to have input request format
        jsonDict = {}
        jsonDict['rid'] = request_id
        jsonDict['numbers'] = pickle.loads(required_request.number_list)
        jsonDict['jobtodo'] = pickle.loads(required_request.jobToDo_list)


        required_numbers = Numbers.query.filter_by(request_id=request_id).all()
        print(len(required_numbers))
        for i in range(0, len(required_numbers)) :
            print(required_numbers[i].id)
        
        return jsonify(jsonDict), 201

@page.route("/check_request", methods=['GET'])
def check_request():
    """
    Check number request and return the status : 
    FAILURE, SUCCESS, PENDING, RECEIVED, REVOKED, RETRY and STARTED (if task is tracked) 
    """
    # import celery app
    from main_app.tasks.tasks import celery
    
    # Get task id from the input request
    task_id = request.json['taskID'] # timeStamp
    
    # Check the status of the celery task 
    res = celery.AsyncResult(task_id)

    return jsonify({'status' : res.status, 'response' : res.result}), 201
    
@page.route("/update_request", methods=['POST'])
def update_request():
    """
    Update tables of our DB after processing 
    """
    from main_app.tasks.tasks import update_number_requests

    # Get data from json request
    number_table_id = request.json['numbers_id'] # list of id inside Numbers table
    numbers_intoRequest = request.json['numbers'] # list of numbers
    #jobToDo_old_intoRequest = request.json['jobtodo_old'] # list of string
    jobToDo_new_intoRequest = request.json['jobtodo_new'] # list of string
    res_intoRequest = request.json['result'] # list of results

    # Invoke celery task to do transaction into the DB
    task = update_number_requests.delay(Ntable_id=number_table_id, N_list=numbers_intoRequest,
                                        JTD_list=jobToDo_new_intoRequest, res_list=res_intoRequest)

    return jsonify({'taskID': task.id}), 201
