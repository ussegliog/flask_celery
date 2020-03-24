# flask_celery

Example of WS Flask with celery tasks

## Instructions

* (For now), Launch redis server :

redis-server

* Launch flask on one terminal

python wsgi_app.py 

* Launch celery on another terminal (with the beat for periodic tasks)

celery worker -A wsgi_app.celery -B --loglevel=info --pool=solo


Two celery tasks with one periodic task and another one with POST request : (curl -X POST http://127.0.0.1:5000/execute_task)
