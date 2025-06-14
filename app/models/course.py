from app import db


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    periods = db.relationship(
        "Period", backref="course", cascade="all, delete", lazy=True
    )

    @staticmethod
    def get_unassigned_courses(course_id, assigned_ids):
        unassigned_courses = Course.query.filter(
            Course.id != course_id, ~Course.id.in_(assigned_ids)
        ).all()
        return unassigned_courses

    @staticmethod
    def get_course_by_id(id):
        course = Course.query.get_or_404(id)
        return course

    @staticmethod
    def get_all_courses():
        courses = Course.query.all()
        return courses

    @staticmethod
    def get_course_by_code(code):
        course = Course.query.filter_by(code=code).first()
        return course
