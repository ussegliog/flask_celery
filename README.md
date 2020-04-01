# flask_celery

Example of WS Flask with celery tasks

## Instructions

* Launch redis server :

**redis-server**

* Launch flask on one terminal

**python wsgi_app.py** 

* Launch celery workers on another terminal (with the beat for periodic tasks)

**celery worker -A wsgi_app.celery -B --loglevel=info --pool=solo**


Two kind of celery tasks are available with periodic tasks and event tasks. The Event tasks can be trigerred by POST or GET requests such as curl -X POST -d "data" http://127.0.0.1:5000/number_request. Two python scripts into test/ repository provide automatic requests and send its to the Web Server. The periodic tasks are scheduled and directly sended by the celery beat.

## Technologies

Several technologies are used inside the code with Flask, Redis, Celery or Flask_SQLAlchemy. Each library has a specific function and the connections between its are described below :


## Code organization



