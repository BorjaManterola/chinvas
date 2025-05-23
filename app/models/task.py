from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    optional = db.Column(db.Boolean, default=False)
    weighting = db.Column(db.Float, nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False)

    grades = db.relationship('Grade', back_populates='task', cascade='all, delete-orphan', passive_deletes=True)
    
    @staticmethod
    def _getSumWeightingInAssessment(assessment_id, exclude_task):
        sum = db.session.query(db.func.sum(Task.weighting)) \
                            .filter(Task.assessment_id == assessment_id, Task.id != exclude_task)
        return sum.scalar() or 0.0

    def isValidWeightingInAssessment(self, new_weighting, exclude_task):
        
        if self.assessment.type_evaluate != 'Percentage':
            return True, 0.0

        weighting_sum = self._getSumWeightingInAssessment(self.assessment.id, exclude_task)
        
        total = weighting_sum + new_weighting
        is_valid = total <= 100 + 1e-5
        return is_valid, total
