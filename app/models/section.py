from app import db

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'), nullable=False)
    code = db.Column(db.Integer)
    type_evaluate = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
