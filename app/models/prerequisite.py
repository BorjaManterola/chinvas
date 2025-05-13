from app import db

class Prerequisite(db.Model):
    __tablename__ = 'prerequisites'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)

    course = db.relationship('Course', foreign_keys=[course_id], cascade="all, delete", backref='prerequisites')
    prerequisite = db.relationship('Course', foreign_keys=[prerequisite_id], backref='prerequisite_of')