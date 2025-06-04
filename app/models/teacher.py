from app import db


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    @staticmethod
    def get_all_teachers():
        teachers = Teacher.query.all()
        return teachers

    @staticmethod
    def get_teacher_by_id(id):
        teacher = Teacher.query.get_or_404(id)
        return teacher
