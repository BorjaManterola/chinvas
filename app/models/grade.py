from app import db


class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    task = db.relationship("Task", back_populates="grades")

    @staticmethod
    def get_grade_by_id(id):
        grade = Grade.query.get_or_404(id)
        return grade

    @staticmethod
    def get_grades_by_task_id(task_id):
        grades = Grade.query.filter_by(task_id=task_id).all()
        return grades

    def get_score(self):
        return self.score

    def set_default_score(self):
        self.score = 1.0

