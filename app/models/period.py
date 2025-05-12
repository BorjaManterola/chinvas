from app import db

class Period(db.Model):
    __tablename__ = 'periods'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10))
    opened = db.Column(db.Boolean, default=True)

    sections = db.relationship('Section', backref='period', cascade='all, delete', lazy=True)