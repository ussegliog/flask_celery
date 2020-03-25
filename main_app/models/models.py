from main_app.extensions import db


class Choice_Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Choice %r>' % self.choice

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, unique=True, nullable=False)
    number_list = db.Column(db.PickleType, unique=False, nullable=False)
    jobToDo_list = db.Column(db.PickleType, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Request %r>' % self.id
