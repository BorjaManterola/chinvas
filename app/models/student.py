from app import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    entry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    grades = db.relationship('Grade', backref='student', lazy=True)
    student_situations = db.relationship('StudentSituation', backref='student', lazy=True)
