from app import db

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    name = db.Column(db.String(255))
    type_evaluate = db.Column(db.String(50))
    weighting = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    tasks = db.relationship("Task", backref="assessment", cascade="all, delete-orphan", passive_deletes=True)
    
    def calculatePercentageSumTasks(self):
        total_percentage = 0
        for task in self.tasks:
            total_percentage += task.weighting
        return total_percentage
    
    def validateWeightingAssessment(self):
        if self.type_evaluate == "Percentage":
            total_percentage = self.calculatePercentageSumTasks()
            if total_percentage != 100:
                return False
        return True
    
    @staticmethod
    def is_valid_weighting(section, new_weighting, exclude_assessment_id=None):
       
        if section.type_evaluate != 'Percentage':
            return True, 0.0

        query = db.session.query(db.func.sum(Assessment.weighting)) \
                          .filter(Assessment.section_id == section.id)

        if exclude_assessment_id:
            query = query.filter(Assessment.id != exclude_assessment_id)

        total = query.scalar() or 0
        is_valid = (total + new_weighting) <= 100
        return is_valid, total
