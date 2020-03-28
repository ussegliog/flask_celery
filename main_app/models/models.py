from main_app.extensions import db

"""
Define tables as models with SQLAlchemy.
Two tables in this example:
_ One to store request and to have a direct interface with views (user APis)
_ Another one to store number and job_to_do. Uses by processing. 
"""

# Request table
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, unique=True, nullable=False)
    number_list = db.Column(db.PickleType, unique=False, nullable=False)
    jobToDo_list = db.Column(db.PickleType, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Request %r>' % self.request_id

# Number table 
class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.Column(db.Integer, unique=False, nullable=False)
    jobToDo = db.Column(db.String(80), unique=False, nullable=False)
    request_id = db.Column(db.Integer, unique=False, nullable=False)
    result_numbers = db.Column(db.Integer, unique=False, nullable=True)
    
    def __repr__(self):
        return '<Numbers %r>' % self.id
