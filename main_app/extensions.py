#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Instanciate a global DB to be available for all elements : views, tasks and models
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


