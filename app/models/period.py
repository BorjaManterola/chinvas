from app import db


class Period(db.Model):
    __tablename__ = "periods"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10))
    opened = db.Column(db.Boolean, default=True)

    sections = db.relationship(
        "Section", backref="period", cascade="all, delete", lazy=True
    )

    @staticmethod
    def get_period_by_id(id):
        period = Period.query.get_or_404(id)
        return period

    @staticmethod
    def get_all_periods():
        periods = Period.query.all()
        return periods

    @staticmethod
    def set_students_final_grades(self):
        for section in self.sections:
            for student_situation in section.student_situations:
                student_situation.set_user_final_grade()

    @staticmethod
    def get_period_by_exact_values(course_id, year, semester):
        period = (
            Period.query.filter_by(
                course_id=course_id, year=year, semester=semester
            )
            .first()
        )
        return period
