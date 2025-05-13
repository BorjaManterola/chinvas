from app import db

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    type_evaluate = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    assessments = db.relationship('Assessment', backref='section', lazy=True)
    student_situations = db.relationship('StudentSituation', backref='section', lazy=True)
    
    def calculatePercentageSumAssessments(self):
        total_percentage = 0
        for assessment in self.assessments:
            total_percentage += assessment.weighting
        return total_percentage
    
    def validateWeightingSection(self):
        if self.type_evaluate == "Percentage":
            total_percentage = self.calculatePercentageSumAssessments()
            if total_percentage != 100:
                return False
        return True
    
    def calculateStudentsSituations(self):
        for assessment in self.assessments:
            if not assessment.validateWeightingAssessment():
                return False
            
        if not self.validateWeightingSection():
            return False
        
        for student_situation in self.student_situations:
            student_situation.calculateFinalGrade()