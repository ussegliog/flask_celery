from main_app.app import celery_app
import random

from main_app.extensions import db
from main_app.models.models import Request
from main_app.models.models import Numbers

import pickle
import subprocess

celery = celery_app

################ Events tasks (with delay and called by views) ###########################
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
    # Put the request into our DB : into request and number tables
    try :

        # First into request table
        my_request = Request(request_id=request_id, number_list=pickle.dumps(number_list),
                             jobToDo_list=pickle.dumps(jobtodo_list))
        db.session.add(my_request)
        
        # Second into number table
        # Loop on number_list and jobtodo_list to store one by one number into number table
        for i in range(0, len(number_list)):
            my_number = Numbers(numbers=number_list[0], jobToDo=jobtodo_list[0],
                                request_id=request_id)
            db.session.add(my_number)
            
        db.session.commit()

    except Exception as exc :
        # Adapt response if exception (usually if rid is already into request table)
        response = "Error during DB transaction : Please Check the request"
        
    return response



@celery.task()
def update_number_requests(Ntable_id, N_list, JTD_list, res_list):

    # List to store request_id for each number
    rId_list = []

    # Update first, Numbers Table and store request id
    for i in range(0, len(Ntable_id)):
        # Query on id
        my_number = Numbers.query.filter_by(id=Ntable_id[i]).first()
        # Update my number
        my_number.jobtodo = JTD_list[i]
        my_number.result_numbers = res_list[i]

        # Store rid for current number
        rId_list.append(my_number.request_id)

        # Save chgts into our DB
        db.session.commit()

    print(rId_list)

    # Udpate then, Request_Table
    for i in range(0, len(rId_list)):
        # Query on request_id
        my_request = Request.query.filter_by(request_id=rId_list[i]).first()

        try :
            # Udpate the right "job to do" with the number index
            ind = pickle.loads(my_request.number_list).index(N_list[i])
            new_JobToDo = pickle.loads(my_request.jobToDo_list)
            new_JobToDo[ind] = JTD_list[i]
            my_request.jobToDo_list = pickle.dumps(new_JobToDo)
            
        except ValueError:
            print("number is not inside the list => no update")

        # Save chgts into our DB
        db.session.commit()

        

################ Periodic tasks/CRON (called by celery beat) ###########################    

# bash commands
def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])


@celery.task()
def periodic_task():

    bash_command('a="Apples and oranges" && echo "${a}"')
    bash_command('sleep 20s && echo "After Pouet \n"')

    #test = Request.query.filter_by(request_id=3).first_or_404()

    #print(pickle.loads(test.number_list))
    
    print('Hi! from periodic_task')
 
#### Processings : with sum and mul operations ####
# Sum
@celery.task()
def sum_task():

    #bash_command('a="Apples and oranges" && echo "${a}"')
    #bash_command('sleep 20s && echo "After Pouet \n"')

    print('Hi! from sum_task')

# Mul
@celery.task()
def mul_task():

    #bash_command('a="Apples and oranges" && echo "${a}"')
    #bash_command('sleep 20s && echo "After Pouet \n"')

    print('Hi! from mul_task')
