from flask import Flask
from celery import Celery
from celery.schedules import crontab

from main_app.celery_task_registry import CELERY_TASK_LIST
from main_app.views.views import page

import os

# Extensions
from main_app.extensions import db

def make_celery(app=None):
    """
    Make Celery App
    :param app: flask app instance
    :return: celery
    """

    #Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    # app.config['CELERYBEAT_SCHEDULE'] = {
    #     # Executes every minute
    #     'periodic_task-every-minute': {
    #         'task': 'periodic_task',
    #         'schedule': crontab(minute="*")
    #     }
    # }
    app.config['result_backend'] = 'redis://localhost:6379/0'
    app.config['beat_schedule'] = {
        # Executes every minute
        "periodic_task-every-minute": {
            "task": "main_app.tasks.tasks.periodic_task",
            "schedule": crontab(minute="*")
        }
    }

    
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update({
        'timezone': 'utc',
        'imports': CELERY_TASK_LIST,
        'result_persistent': False,
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json']})

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    # To register our view
    app.register_blueprint(page)
    
    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates app instance passed in)
    :param app: flask app
    :return: None
    """
    db.init_app(app)

    return None

flask_app = create_app()
celery_app = make_celery(flask_app)
