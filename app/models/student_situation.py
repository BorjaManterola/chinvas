from app import db
from app.models.grade import Grade
from app.models.task import Task


class StudentSituation(db.Model):
    __tablename__ = "student_situations"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(
        db.Integer,
        db.ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    final_grade = db.Column(db.Numeric(2, 1))

    @staticmethod
    def get_student_situation_by_id(id):
        student_situation = StudentSituation.query.get_or_404(id)
        return student_situation

    @staticmethod
    def get_assigned_students_ids_in_section(section_id):
        student_situations_ids = (
            db.session.query(StudentSituation.student_id)
            .filter_by(section_id=section_id)
            .all()
        )

        assigned_ids = {id for (id,) in student_situations_ids}

        return assigned_ids

    def get_user_tasks_in_section(self):
        tasks = []
        for assessment in self.section.assessments:
            tasks += self.get_assessment_tasks(assessment)
        return tasks

    def get_user_grades_in_section(self):
        grades = []
        for assessment in self.section.assessments:
            grades += self.get_user_grades_in_asessment(assessment)
        return grades

    @staticmethod
    def get_assessment_tasks(assessment):
        tasks = (
            db.session.query(Task).filter_by(assessment_id=assessment.id).all()
        )
        return tasks

    def set_user_final_grade(self):
        final_grade = self.calculate_final_grade()
        self.final_grade = final_grade
        db.session.commit()

    def calculate_final_grade(self):
        assessments = self.section.assessments
        total_weighting = sum(
            assessment.weighting for assessment in assessments
        )
        sum_ponderates_grades = 0.0
        for assessment in assessments:
            final_grade_of_assessment = (
                self.get_user_final_grade_in_assessment(assessment)
            )
            sum_ponderates_grades += (
                final_grade_of_assessment * assessment.weighting
            )
        final_grade = sum_ponderates_grades / total_weighting
        return final_grade

    def get_user_final_grade_in_assessment(self, assessment):
        tasks = self.get_assessment_tasks(assessment)
        grades = self.get_user_grades_in_asessment(assessment)
        total_weighting = sum(task.weighting for task in tasks)
        sum_ponderates_grades = 0.0
        for grade in grades:
            for task in tasks:
                if grade.task_id == task.id:
                    if task.optional and grade.score is None:
                        continue
                    elif not task.optional and grade.score is None:
                        grade.score = 1.0
                    sum_ponderates_grades += grade.score * task.weighting

        final_grade_of_assessment = sum_ponderates_grades / total_weighting
        return final_grade_of_assessment

    def get_user_grades_in_asessment(self, assessment):
        grades = []
        for task in assessment.tasks:
            grade = self.get_grade_by_student_id_and_task_id(
                self.student_id, task.id
            )
            if grade:
                grades.append(grade)
        return grades

    @staticmethod
    def get_grade_by_student_id_and_task_id(student_id, task_id):
        grade = (
            db.session.query(Grade)
            .filter_by(student_id=student_id, task_id=task_id)
            .first()
        )
        return grade
