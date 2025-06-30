from app import db
from app.models.section import Section
from app.models.task import Task


class Assessment(db.Model):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(
        db.Integer,
        db.ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = db.Column(db.String(255))
    type_evaluate = db.Column(db.String(50))
    weighting = db.Column(db.Float)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    tasks = db.relationship(
        "Task",
        backref="assessment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @staticmethod
    def get_sum_weighting_in_section(section_id, exclude_assessment):
        sum_ = db.session.query(db.func.sum(Assessment.weighting)).filter(
            Assessment.section_id == section_id,
            Assessment.id != exclude_assessment,
        )
        return sum_.scalar() or 0.0

    def is_valid_weighting_in_section(self, new_weighting, exclude_assessment):
        if self.section.type_evaluate != "Percentage":
            return True, 0.0

        weighting_sum = self.get_sum_weighting_in_section(
            self.section.id, exclude_assessment
        )
        total = weighting_sum + new_weighting
        is_valid = total <= 100 + 1e-5
        return is_valid, total

    @staticmethod
    def get_assessment_by_id(id):
        assessment = Assessment.query.get_or_404(id)
        return assessment

    @staticmethod
    def get_assessment_tasks(id):
        tasks = db.session.query(Task).filter_by(assessment_id=id).all()
        return tasks

    @staticmethod
    def get_assessment_section(id):
        assessment = Assessment.get_assessment_by_id(id)
        section = db.session.query(Section).get_or_404(assessment.section_id)
        return section

    def get_assessment_weighting(self):
        return self.weighting

