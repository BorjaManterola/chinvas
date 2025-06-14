from app import db


class Classroom(db.Model):
    __tablename__ = "classroom"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    @staticmethod
    def get_classroom(id):
        classroom = Classroom.query.get_or_404(id)
        return classroom

    @staticmethod
    def get_all_classrooms():
        classrooms = Classroom.query.all()
        return classrooms
