from app import db

class StudentSituation(db.Model):
    __tablename__ = 'student_situations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    final_grade = db.Column(db.Numeric(2, 1))

    