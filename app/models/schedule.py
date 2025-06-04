import io
from datetime import time

from flask import send_file
from openpyxl import Workbook
from sqlalchemy.orm import joinedload

from app import db
from app.models.class_ import Class
from app.models.classroom import Classroom
from app.models.period import Period
from app.models.section import Section
from app.models.student_situation import StudentSituation


class Schedule(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    classes = db.relationship(
        "Class", backref="schedule", cascade="all, delete", lazy=True
    )

    def generate_schedule(self):
        sections = self._get_sections()
        classrooms = Schedule.get_all_classrooms()
        availability = self._build_availability_matrix(classrooms)

        classes_to_create = []
        unassigned_sections = []

        for section in sections:
            result = self._assign_section(section, classrooms, availability)
            if result["assigned"]:
                classes_to_create.append(result["class_data"])
            else:
                unassigned_sections.append(result["error"])

        return {
            "classes_to_create": classes_to_create,
            "unassigned_sections": unassigned_sections,
        }

    @staticmethod
    def get_all_classrooms():
        return db.session.query(Classroom).all()

    def _get_sections(self):
        return (
            db.session.query(Section)
            .join(Period)
            .options(
                joinedload(Section.period).joinedload(Period.course),
                joinedload(Section.student_situations).joinedload(
                    StudentSituation.student
                ),
                joinedload(Section.teacher),
            )
            .filter(Period.year == self.year, Period.semester == self.semester)
            .all()
        )

    @staticmethod
    def _build_availability_matrix(classrooms):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        modules = [9, 10, 11, 12, 14, 15, 16, 17]
        return {
            day: {
                hour: {room.id: True for room in classrooms}
                for hour in modules
            }
            for day in days
        }

    @staticmethod
    def _has_conflict(day, block, section):
        block_start = time(block[0])
        block_end = time(block[-1] + 1)

        existing_classes = Schedule.get_classes_occuring_on_block(
            day, block_start, block_end
        )

        for existing_class in existing_classes:
            if existing_class.section.teacher_id == section.teacher_id:
                return True

            existing_students = {
                student.id
                for student in existing_class.section.get_section_students()
            }
            current_students = {
                student.id for student in section.get_section_students()
            }
            has_common_students = existing_students & current_students
            if has_common_students:
                return True

        return False

    @staticmethod
    def get_classes_occuring_on_block(day, block_start, block_end):
        return Class.query.filter(
            Class.day_of_week == day,
            Class.start_time < block_end,
            Class.end_time > block_start,
        ).all()

    def _assign_section(self, section, classrooms, availability):
        modules = [9, 10, 11, 12, 14, 15, 16, 17]
        students = section.get_section_students()
        blocks_needed = section.period.course.credits

        assigned_section = self._block_limit_check(section)
        if assigned_section:
            return assigned_section

        result = self._find_available_assignment(
            section, classrooms, availability, modules, blocks_needed, students
        )
        if result:
            day, block, room = result
            self._mark_availability(availability, day, block, room)
            class_data = self._build_class_data(section, block, day, room)
            self.create_schedule_class(class_data)
            return {"assigned": True, "class_data": class_data}

        return self._availability_assignment_error(section)

    def _find_available_assignment(
        self,
        section,
        classrooms,
        availability,
        modules,
        blocks_needed,
        students,
    ):
        for day in self._get_days():
            for i in range(len(modules) - blocks_needed + 1):
                block = modules[i : i + blocks_needed]
                if 13 in block:
                    continue
                for room in classrooms:
                    if room.capacity < len(students):
                        continue
                    if self.check_availability(
                        availability, block, day, room.id, section
                    ):
                        return day, block, room
        return None

    def _mark_availability(self, availability, day, block, room):
        for h in block:
            availability[day][h][room.id] = False

    def check_availability(self, availability, block, day, room_id, section):
        return all(
            availability[day][h][room_id] for h in block
        ) and not self._has_conflict(day, block, section)

    def _block_limit_check(self, section):
        if section.period.course.credits > 4:
            return {
                "assigned": False,
                "error": {
                    "section_id": section.id,
                    "reason": "More than 4 consecutive blocks required",
                },
            }
        else:
            return {}

    def _get_days(self):
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    def _build_class_data(self, section, block, day, room):
        return {
            "section_id": section.id,
            "day_of_week": day,
            "start_time": time(block[0]),
            "end_time": time(block[-1] + 1),
            "classroom_id": room.id,
            "schedule_id": self.id,
        }

    def _availability_assignment_error(self, section):
        return {
            "assigned": False,
            "error": {
                "section_id": section.id,
                "reason": "No available time slots or rooms",
            },
        }

    def export_schedule_to_excel(self):
        try:
            data_rows = self._build_excel_rows()
        except Exception as e:
            raise RuntimeError(f"Error building Excel rows: {str(e)}")

        wb = Workbook()
        ws = wb.active
        ws.title = "Schedule"

        headers = [
            "Course",
            "Section ID",
            "Teacher",
            "Classroom",
            "Day",
            "Start Time",
            "End Time",
        ]
        ws.append(headers)

        for row in data_rows:
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"schedule_{self.year}_{self.semester}.xlsx",
        )

    def _build_excel_rows(self):
        rows = []
        classes = Class.query.filter_by(schedule_id=self.id).all()

        for cls in classes:
            try:
                course_name = cls.section.period.course.name
                section_id = cls.section.id
                teacher_name = cls.section.teacher.name
                classroom_name = cls.classroom.name
                day_of_week = cls.day_of_week
                start = cls.start_time.strftime("%H:%M")
                end = cls.end_time.strftime("%H:%M")
                rows.append(
                    [
                        course_name,
                        section_id,
                        teacher_name,
                        classroom_name,
                        day_of_week,
                        start,
                        end,
                    ]
                )
            except AttributeError:
                raise ValueError(
                    f"Incomplete class data for class ID {cls.id}"
                )
        return rows

    @staticmethod
    def validate_inputs(year, semester):
        if not year or not semester:
            return False, "Year and semester are required."
        try:
            int(year)
        except ValueError:
            return False, "Year must be a number."
        return True, None

    @staticmethod
    def schedule_exists(year, semester):
        return (
            Schedule.query.filter_by(year=year, semester=semester).first()
            is not None
        )

    @staticmethod
    def build_schedule(year, semester):
        schedule = Schedule(year=year, semester=semester)
        db.session.add(schedule)
        db.session.flush()
        return schedule

    def find_class(
        self, section_id, day_of_week, start_time, end_time, classroom_id
    ):
        return Class.query.filter_by(
            section_id=section_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            classroom_id=classroom_id,
            schedule_id=self.id,
        ).first()

    def create_schedule_class(self, class_data):
        new_class = Class(
            section_id=class_data["section_id"],
            day_of_week=class_data["day_of_week"],
            start_time=class_data["start_time"],
            end_time=class_data["end_time"],
            classroom_id=class_data["classroom_id"],
            schedule_id=self.id,
        )
        db.session.add(new_class)
        db.session.flush()
        db.session.commit()

    def create_schedule_classes(self, classes_to_create, schedule_id):
        for c in classes_to_create:
            existing_class = self.find_class(
                section_id=c["section_id"],
                day_of_week=c["day_of_week"],
                start_time=c["start_time"],
                end_time=c["end_time"],
                classroom_id=c["classroom_id"],
            )

            if not existing_class:
                new_class = Class(
                    section_id=c["section_id"],
                    day_of_week=c["day_of_week"],
                    start_time=c["start_time"],
                    end_time=c["end_time"],
                    classroom_id=c["classroom_id"],
                    schedule_id=schedule_id,
                )
                db.session.add(new_class)
                db.session.flush()
        db.session.commit()

    @staticmethod
    def handle_schedule_creation(year, semester):
        is_valid, error_message = Schedule.validate_inputs(year, semester)
        if not is_valid:
            return None, error_message

        year = int(year)
        if Schedule.schedule_exists(year, semester):
            return (
                None,
                f"A schedule for year {year} and semester '{semester}' already exists.",
            )

        schedule = Schedule.build_schedule(year, semester)
        result = schedule.generate_schedule()

        if not result["unassigned_sections"]:
            schedule.create_schedule_classes(
                result["classes_to_create"], schedule.id
            )
            return schedule, None
        else:
            db.session.rollback()
            errors = ["⚠ Could not generate schedule due to conflicts:"]
            for s in result["unassigned_sections"]:
                errors.append(f"Section {s['section_id']}: {s['reason']}")
            return None, "<br>".join(errors)
