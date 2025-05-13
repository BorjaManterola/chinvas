from app import db
from app.models.section import Section
from app.models.classroom import Classroom
from app.models.class_ import Class
from sqlalchemy.orm import joinedload
from app.models.teacher import Teacher
from app.models.period import Period
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.student import Student
from app.models.student_situation import StudentSituation
from datetime import time
from app.models.course import Course

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    classes = db.relationship("Class", backref="schedule", cascade="all, delete", lazy=True)

    def generate_schedule(self):
        DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        MODULES = [9, 10, 11, 12, 14, 15, 16, 17]
        MAX_CONSECUTIVE = 4

        sections = db.session.query(Section).\
            join(Period).\
            options(
                joinedload(Section.period).joinedload(Period.course),
                joinedload(Section.student_situations).joinedload(StudentSituation.student)
            ).\
            filter(Period.year == self.year, Period.semester == self.semester).\
            all()

        classrooms = Classroom.query.all()

        availability = {
            day: {
                hour: {room.id: True for room in classrooms} for hour in MODULES
            } for day in DAYS
        }

        classes_to_create = []
        unassigned_sections = []

        for section in sections:
            assigned = False
            blocks_needed = section.period.course.credits
            students = section.getStudents()

            if blocks_needed > MAX_CONSECUTIVE:
                unassigned_sections.append({
                    "section_id": section.id,
                    "reason": "More than 4 consecutive blocks required"
                })
                continue

            for day in DAYS:
                for i in range(len(MODULES) - blocks_needed + 1):
                    block = MODULES[i:i + blocks_needed]
                    if 13 in block:
                        continue

                    for room in classrooms:
                        if room.capacity < len(students):
                            continue

                        if all(availability[day][h][room.id] for h in block):
                            conflict = False

                            for h in block:
                                start = time(h)
                                existing_classes = Class.query.filter_by(
                                    day_of_week=day,
                                    start_time=start
                                ).all()
                                for existing in existing_classes:
                                    if existing.section_id == section.id:
                                        conflict = True
                                        break
                                if conflict:
                                    break

                            if conflict:
                                continue

                            for h in block:
                                availability[day][h][room.id] = False

                            classes_to_create.append({
                                "section_id": section.id,
                                "day_of_week": day,
                                "start_time": time(block[0]),
                                "end_time": time(block[-1] + 1),
                                "classroom_id": room.id,
                                "schedule_id": self.id
                            })
                            assigned = True
                            break
                    if assigned:
                        break
                if assigned:
                    break

            if not assigned:
                unassigned_sections.append({
                    "section_id": section.id,
                    "reason": "No available block without conflict"
                })

        return {
            "classes_to_create": classes_to_create,
            "unassigned_sections": unassigned_sections
        }
