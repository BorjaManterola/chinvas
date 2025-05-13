from app import db

class Prerequisite(db.Model):
    __tablename__ = 'prerequisites'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)

    course = db.relationship('Course', foreign_keys=[course_id], backref=db.backref('prerequisites', cascade="all, delete-orphan", lazy=True))
    prerequisite = db.relationship('Course', foreign_keys=[prerequisite_id], backref=db.backref('prerequisite_of', cascade="all, delete-orphan", lazy=True))