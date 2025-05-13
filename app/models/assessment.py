from app import db

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255))
    type_evaluate = db.Column(db.String(50))
    weighting = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    tasks = db.relationship("Task", backref="assessment", cascade="all, delete-orphan", passive_deletes=True)
    
    @staticmethod
    def _getSumWeightingInSection(section_id, exclude_assessment):
        if exclude_assessment:
            sum = db.session.query(db.func.sum(Assessment.weighting)) \
                              .filter(Assessment.section_id == section_id, Assessment.id != exclude_assessment)
        else:
            sum = db.session.query(db.func.sum(Assessment.weighting)) \
                            .filter(Assessment.section_id == section_id)
        return sum
        
    def isValidWeightingInSection(self, section, new_weighting, exclude_assessment=None):
        if section.type_evaluate != 'Percentage':
            return True, 0.0

        weighting_sum = self._getSumWeightingInSection(section.id, exclude_assessment)

        total = weighting_sum + new_weighting
        is_valid = total <= 100
        return is_valid, total
