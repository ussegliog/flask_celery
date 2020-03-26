from main_app.app import celery_app
import random

from main_app.extensions import db
from main_app.models.models import Choice_Task
from main_app.models.models import Request

import pickle
import subprocess

celery = celery_app


@celery.task(bind=True)
def my_task(self):
    choice = random.choice(['Alpha',
                            'Beta',
                            'Gamma',
                            'Delta',
                            'Epsilon',
                            'Zeta',
                            'Eta',
                            'Theta',
                            'Iota',
                            'Kappa',
                            'Lambda',
                            'Mu',
                            'Nu',
                            'Xi',
                            'Omicron',
                            'Pi',
                            'Rho',
                            'Sigma',
                            'Tau',
                            'Upsilon',
                            'Phi',
                            'Chi',
                            'Psi',
                            'Omega'])

    return choice

@celery.task()
def handle_number_requests(request_id, number_list, jobtodo_list):

    response = "OK"
    # Put the request into our DB
    try :
        my_request = Request(request_id=request_id, number_list=pickle.dumps(number_list),
                         jobToDo_list=pickle.dumps(jobtodo_list))
        db.session.add(my_request)
        db.session.commit()

        print(pickle.loads(my_request.number_list))
    except Exception as exc :
        response = "Error during DB transaction : Please Check the request"
        
    return response





def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

@celery.task()
def periodic_task():

    bash_command('a="Apples and oranges" && echo "${a}"')
    bash_command('sleep 20s && echo "After Pouet \n"')

    test = Request.query.filter_by(request_id=3).first_or_404()

    print(pickle.loads(test.number_list))
    
    print('Hi! from periodic_task')
 
