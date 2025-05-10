from app import db

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    score = db.Column(db.Numeric(2, 1))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
