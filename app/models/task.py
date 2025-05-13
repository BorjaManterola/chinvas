from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    optional = db.Column(db.Boolean, default=False)
    weighting = db.Column(db.Float, nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False)

    grades = db.relationship('Grade', back_populates='task', cascade='all, delete-orphan', passive_deletes=True)

    def isValidWeightingAssessment(self, cls, assessment_id, new_weighting, exclude_task_id=None):
        query = db.session.query(db.func.sum(cls.weighting)).filter_by(assessment_id=assessment_id)
        if exclude_task_id:
            query = query.filter(cls.id != exclude_task_id)

        current_total = query.scalar() or 0
        if current_total + new_weighting > 100:
            return False, current_total
        return True, current_total
