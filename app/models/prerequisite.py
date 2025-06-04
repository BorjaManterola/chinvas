from app import db


class Prerequisite(db.Model):
    __tablename__ = "prerequisites"
    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    prerequisite_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )

    course = db.relationship(
        "Course",
        foreign_keys=[course_id],
        backref=db.backref(
            "prerequisites", cascade="all, delete-orphan", lazy=True
        ),
    )
    prerequisite = db.relationship(
        "Course",
        foreign_keys=[prerequisite_id],
        backref=db.backref(
            "prerequisite_of", cascade="all, delete-orphan", lazy=True
        ),
    )

    @staticmethod
    def get_prerequisite_by_id(id):
        prerequisite = Prerequisite.query.get_or_404(id)
        return prerequisite

    @staticmethod
    def get_assigned_courses_ids(id):
        courses_ids = {
            id
            for (id,) in db.session.query(Prerequisite.prerequisite_id)
            .filter_by(course_id=id)
            .all()
        }
        return courses_ids

    @staticmethod
    def get_prerequisite_by_course_id_and_id(id, course_id):
        exist_prerequisite = Prerequisite.query.filter_by(
            course_id=course_id, prerequisite_id=id
        ).first()
        return exist_prerequisite
