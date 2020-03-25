from main_app.app import (flask_app,
                          celery_app,
                          db)

import sqlite3

app = flask_app
celery = celery_app


# def db_connect(db_path=app.config['DB_PATH']):
#     con = sqlite3.connect(db_path)
#     return con


# # Initialize a sqlite3 database
# db_connect()


if __name__ == "__main__":
    print("Pouet \n")
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    app.run(debug=True)
