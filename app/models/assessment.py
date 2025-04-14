from app import db

class Assessment(db.Model):
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    name = db.Column(db.String(255))
    type_evaluate = db.Column(db.String(50))
    weighting = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    
    tasks = db.relationship("Task", cascade="all, delete-orphan")
