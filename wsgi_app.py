#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Main script (run our Flask application)
"""

from main_app.app import (flask_app,
                          celery_app,
                          db)


app = flask_app
celery = celery_app


if __name__ == "__main__":
    app.run(debug=True)
