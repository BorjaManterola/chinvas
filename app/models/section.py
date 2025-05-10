from app import db

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    type_evaluate = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    assessments = db.relationship('Assessment', backref='section', lazy=True)
    student_situations = db.relationship('StudentSituation', backref='section', lazy=True)