from app import db

class UserSituation(db.Model):
    __tablename__ = 'usersituations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    situation = db.Column(db.String(20), nullable=False)  # "teacher", "student", etc.
    final_grade = db.Column(db.Float, nullable=True)

    user = db.relationship("User")
    section = db.relationship("Section", back_populates="usersituations")

