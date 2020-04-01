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

![Technologies : ](./img/Technos.png?raw=true "Technology connections")


First of all, Flask server receives and handles incoming http requests. Celery is a task queue implementation for Python web applications used to asynchronously execute work outside the HTTP request-response cycle. Periodic tasks can also be executed thanks to the beat. Celery uses a message broker for the communication between tasks (redis here). Eventually, the ORM Flask_SQLAlchamy provides a generic API to make transactions with several kind of databases (PostGres, MySQL, Sqlite ...). For this code, a sqlite database is settled.  


## Code organization

![FlaskCelery directory : ](./img/Rep_FlaskCelery.png?raw=true "FlaskCelery directory/")


The Flask server is put at the center with four directories to add specific features or tests/processings :
* *config/* : Define global path or configuration
* *test/* : Simulate user requests
* *processings/* : Define simple processings (python scripts)
* *main_app/* : Main diretory to initialize/instanciate Flask/Celery applications and to handle incoming requests.
The main_app repository contains the heart of source files, with the following organization:


![MainApp directory : ](./img/Rep_mainApp.png?raw=true "MainApp directory/")



Two parts are displayed. On one hand, we find the initialization/configuration of applications or extensions. On the other hand, we can make out all mechanisms to handle requests, periodic tasks and DB transactions with :
* *models* : Specify DB Tables
* *views* : Define available views for the Web Server
* *tasks* : Implement celery tasks (asynchronous and periodic)


