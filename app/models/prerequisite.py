from app import db

class Prerequisite(db.Model):
    __tablename__ = 'prerequisites'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'), nullable=False)
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
