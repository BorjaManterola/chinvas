from app import db

class UserSituation(db.Model):
    __tablename__ = 'usersituations'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), primary_key=True)
    situation = db.Column(db.String(50))
    final_grade = db.Column(db.Float)
