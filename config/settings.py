# DEV settings.py
import os
from pathlib import Path

DEBUG = True

# Secret key
SECRET_KEY = os.urandom(24)

# Database Path
DB_PATH = os.path.join(Path(__file__).parent.parent, 'database.sqlite3')

# SQL Alchemy Database URI
SQL_ALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"



