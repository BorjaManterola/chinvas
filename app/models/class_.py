from app import db

class Class(db.Model):
    __tablename__ = 'class'

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id', ondelete='CASCADE'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', name='days_of_week'),nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    section = db.relationship("Section", backref=db.backref("classes", cascade="all, delete", lazy=True))
    classroom = db.relationship("Classroom", backref="classes")

    @staticmethod
    def get_class_by_id(id):
        class_instance = Class.query.get_or_404(id)
        return class_instance

    @staticmethod
    def get_all_classes():
        classes = Class.query.all()
        return classes