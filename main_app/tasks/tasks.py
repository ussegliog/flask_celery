from main_app.app import celery_app
import random

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


def bash_command(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd])

@celery.task()
def periodic_task():

    bash_command('a="Apples and oranges" && echo "${a}"')
    bash_command('sleep 20s && echo "After Pouet \n"')
    print('Hi! from periodic_task')
 
