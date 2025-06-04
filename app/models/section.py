from app import db


class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(
        db.Integer,
        db.ForeignKey("periods.id", ondelete="CASCADE"),
        nullable=False,
    )
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
    )
    type_evaluate = db.Column(db.String(50))
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    assessments = db.relationship(
        "Assessment",
        backref="section",
        lazy=True,
        cascade="all, delete-orphan",
    )
    student_situations = db.relationship(
        "StudentSituation",
        backref="section",
        lazy=True,
        cascade="all, delete-orphan",
    )
    teacher = db.relationship(
        "Teacher",
        backref=db.backref("sections", cascade="all, delete", lazy=True),
    )

    def get_section_students(self):
        return [ss.student for ss in self.student_situations]

    @staticmethod
    def get_section_by_id(id):
        section = Section.query.get_or_404(id)
        return section

    @staticmethod
    def get_all_sections():
        sections = Section.query.all()
        return sections
