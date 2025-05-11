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