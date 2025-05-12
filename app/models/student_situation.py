from app import db

class StudentSituation(db.Model):
    __tablename__ = 'student_situations'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    final_grade = db.Column(db.Numeric(2, 1))

    student = db.relationship('Student', backref='student_situations')

    def calculateFinalGrade(self):
        print("Calculating final grade for student situation")