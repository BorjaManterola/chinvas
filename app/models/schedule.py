from app import db

class Schedule(db.Model):
    __tablename__ = 'schedule'
    
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.Enum('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', name='days_of_week'), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relaciones
    section = db.relationship('Section', back_populates='schedules')
    classroom = db.relationship('Classroom', back_populates='schedules')

    __table_args__ = (
        db.UniqueConstraint('section_id', 'day_of_week', 'start_time', name='unique_section_schedule'),
        db.UniqueConstraint('classroom_id', 'day_of_week', 'start_time', 'end_time', name='unique_classroom_schedule')
    )
