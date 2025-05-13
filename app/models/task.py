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
        if exclude_task:
            sum = db.session.query(db.func.sum(Task.weighting)) \
                              .filter(Task.assessment_id == assessment_id, Task.id != exclude_task)
        else:
            sum = db.session.query(db.func.sum(Task.weighting)) \
                            .filter(Task.assessment_id == assessment_id)
        return sum

    def isValidWeightingInAssessment(self, assessment, new_weighting, exclude_task=None):
        
        if assessment.type_evaluate != 'Percentage':
            return True, 0.0

        weighting_sum = self._getSumWeightingInAssessment(assessment.id, exclude_task)
        
        total = weighting_sum + new_weighting

        is_valid = total <= 100
        return is_valid, total
