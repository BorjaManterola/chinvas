from app import db

class Member(db.Model):
    __tablename__ = 'members'
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
