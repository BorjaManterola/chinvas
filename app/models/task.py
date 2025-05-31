from app import db


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    optional = db.Column(db.Boolean, default=False)
    weighting = db.Column(db.Float, nullable=False)
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
    )

    grades = db.relationship(
        "Grade",
        back_populates="task",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @staticmethod
    def get_sum_weighting_in_assessment(assessment_id, exclude_task):
        sum = db.session.query(db.func.sum(Task.weighting)).filter(
            Task.assessment_id == assessment_id, Task.id != exclude_task
        )
        return sum.scalar() or 0.0

    def is_valid_weighting_in_assessment(self, new_weighting, exclude_task):
        if self.assessment.type_evaluate != "Percentage":
            return True, 0.0

        weighting_sum = self.get_sum_weighting_in_assessment(
            self.assessment.id, exclude_task
        )

        total_weight = weighting_sum + new_weighting
        is_valid_weight = total_weight <= 100 + 1e-5
        return is_valid_weight, total_weight
