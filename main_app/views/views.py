from flask import current_app as app
from flask import (Blueprint,
                   render_template,
                   request,
                   jsonify)



#import sqlite3
#import pandas as pd

from main_app.extensions import db
from main_app.models.models import Choice_Task
from main_app.models.models import Request

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

    choice_intoRequest = request.json['choice']

    
    # Put something into our DB
    my_choice = Choice_Task(choice=choice_intoRequest)
    db.session.add(my_choice)
    db.session.commit()

    db.session.flush()

    return jsonify({'taskID': task.id}), 201

@page.route("/number_request", methods=['POST'])
def number_task():
    """
    Invoke this function from an Ajax Call
    :return: json
    """  
    from main_app.tasks.tasks import handle_number_requests

    request_id = request.json['rid'] # int
    numbers_intoRequest = request.json['numbers'] # list of numbers
    jobToDo_intoRequest = request.json['jobtodo'] # list of string
    
    if request.method == 'POST':
        # Invoke celery task
        task = handle_number_requests.delay(request_id=request_id,
                                            number_list=numbers_intoRequest,
                                            jobtodo_list=jobToDo_intoRequest)
        
    return task.id

@page.route("/get_task", methods=['GET'])
def _get_task():
    test = Choice_Task.query.filter_by(choice='RePouet').first_or_404()

    print(test.id)
    return test.choice
