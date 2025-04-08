from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    assesstment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    name = db.Column(db.String(255))
    optional = db.Column(db.Boolean)
    weighting = db.Column(db.Integer)
    date = db.Column(db.Date)
