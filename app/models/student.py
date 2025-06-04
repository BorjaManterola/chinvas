from app import db


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    entry_date = db.Column(db.Date)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    grades = db.relationship(
        "Grade", backref="student", cascade="all, delete", lazy=True
    )
    student_situations = db.relationship(
        "StudentSituation", backref="student", cascade="all, delete", lazy=True
    )

    @staticmethod
    def get_student_by_id(id):
        student = Student.query.get_or_404(id)
        return student

    @staticmethod
    def get_all_students():
        students = Student.query.all()
        return students

    @staticmethod
    def get_available_students(assigned_ids):
        students = Student.query.filter(~Student.id.in_(assigned_ids)).all()
        return students
