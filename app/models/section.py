from app import db

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'), nullable=False)
    nrc = db.Column(db.Integer, nullable=False)
    type_evaluate = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    usersituations = db.relationship("UserSituation", back_populates="section", cascade="all, delete-orphan")