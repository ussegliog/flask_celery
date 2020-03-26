from main_app.app import (flask_app,
                          celery_app,
                          db)

import sqlite3

app = flask_app
celery = celery_app


if __name__ == "__main__":
    app.run(debug=True)
