from app import db

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    periods = db.relationship("Period", backref="course", cascade="all, delete", lazy=True)