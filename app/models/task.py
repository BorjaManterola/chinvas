from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    optional = db.Column(db.Boolean, default=False)
    weighting = db.Column(db.Float, nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False)

    grades = db.relationship('Grade', back_populates='task', cascade='all, delete-orphan', passive_deletes=True)
