from app import db
from app.models.section import Section
from app.models.classroom import Classroom
from app.models.class_ import Class
from app.models.period import Period
from app.models.student_situation import StudentSituation
from sqlalchemy.orm import joinedload
from datetime import time
from openpyxl import Workbook
import io
from flask import send_file

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    classes = db.relationship("Class", backref="schedule", cascade="all, delete", lazy=True)

    def generateSchedule(self):
        sections = self._getSections()
        classrooms = Classroom.query.all()
        availability = self._buildAvailabilityMatrix(classrooms)

        classes_to_create = []
        unassigned_sections = []

        for section in sections:
            result = self._assignSection(section, classrooms, availability)
            if result["assigned"]:
                classes_to_create.append(result["class_data"])
            else:
                unassigned_sections.append(result["error"])

        return {
            "classes_to_create": classes_to_create,
            "unassigned_sections": unassigned_sections
        }

    def _getSections(self):
        return db.session.query(Section).            join(Period).            options(
                joinedload(Section.period).joinedload(Period.course),
                joinedload(Section.student_situations).joinedload(StudentSituation.student),
                joinedload(Section.teacher)
            ).            filter(Period.year == self.year, Period.semester == self.semester).            all()

    def _buildAvailabilityMatrix(self, classrooms):
        DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        MODULES = [9, 10, 11, 12, 14, 15, 16, 17]
        return {
            day: {hour: {room.id: True for room in classrooms} for hour in MODULES}
            for day in DAYS
        }

    def _hasConflict(self, day, block, section):
        for h in block:
            existing_classes = Class.query.filter_by(
                day_of_week=day,
                start_time=time(h)
            ).all()

            for existing in existing_classes:
                if existing.section.teacher_id == section.teacher_id:
                    return True

                existing_students = {s.id for s in existing.section.getSectionStudents()}
                current_students = {s.id for s in section.getSectionStudents()}
                if existing_students & current_students:
                    return True

        return False

    def _assignSection(self, section, classrooms, availability):
        DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        MODULES = [9, 10, 11, 12, 14, 15, 16, 17]
        MAX_CONSECUTIVE = 4

        blocks_needed = section.period.course.credits
        students = section.getSectionStudents()

        if blocks_needed > MAX_CONSECUTIVE:
            return {"assigned": False, "error": {
                "section_id": section.id,
                "reason": "More than 4 consecutive blocks required"
            }}

        for day in DAYS:
            for i in range(len(MODULES) - blocks_needed + 1):
                block = MODULES[i:i + blocks_needed]
                if 13 in block:
                    continue

                for room in classrooms:
                    if room.capacity < len(students):
                        continue

                    if all(availability[day][h][room.id] for h in block) and not self._hasConflict(day, block, section):
                        for h in block:
                            availability[day][h][room.id] = False

                        return {
                            "assigned": True,
                            "class_data": {
                                "section_id": section.id,
                                "day_of_week": day,
                                "start_time": time(block[0]),
                                "end_time": time(block[-1] + 1),
                                "classroom_id": room.id,
                                "schedule_id": self.id
                            }
                        }

        return {"assigned": False, "error": {
            "section_id": section.id,
            "reason": "No available block without conflict"
        }}

    def exportScheduleToExcel(self):
        try:
            data_rows = self._buildExcelRows()
        except Exception as e:
            raise RuntimeError(f"Error building Excel rows: {str(e)}")

        wb = Workbook()
        ws = wb.active
        ws.title = "Schedule"

        headers = ["Course", "Section", "Classroom", "Start Time", "End Time"]
        ws.append(headers)

        for row in data_rows:
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'schedule_{self.year}_{self.semester}.xlsx'
        )

    def _buildExcelRows(self):
        rows = []
        classes = Class.query.filter_by(schedule_id=self.id).all()

        for cls in classes:
            try:
                course_name = cls.section.period.course.name
                section_id = cls.section.id
                classroom_name = cls.classroom.name
                start = cls.start_time.strftime("%H:%M")
                end = cls.end_time.strftime("%H:%M")
                rows.append([course_name, section_id, classroom_name, start, end])
            except AttributeError:
                raise ValueError(f"Incomplete class data for class ID {cls.id}")
        return rows
