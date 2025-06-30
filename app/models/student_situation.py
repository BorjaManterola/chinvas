from typing import List

from app import db
from app.models.assessment import Assessment
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
    def get_student_situation_by_exact_values(section_id, student_id):
        student_situation = (
            db.session.query(StudentSituation)
            .filter_by(section_id=section_id, student_id=student_id)
            .first()
        )
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

    def get_student_situation_assessments(self):
        assessments = self.section.assessments
        return assessments

    def get_user_tasks_in_section(self):
        tasks = []
        for assessment in self.section.assessments:
            tasks += self.get_assessment_tasks(assessment)
        return tasks

    def get_user_grades_in_section(self):
        grades = []
        for assessment in self.section.assessments:
            grades += self.get_user_situation_grades_in_asessment(assessment)
        return grades

    @staticmethod
    def get_assessment_tasks(assessment):
        tasks = (
            db.session.query(Task).filter_by(assessment_id=assessment.id).all()
        )
        return tasks

    def set_user_situation_final_grade(self):
        final_grade = self.calculate_final_grade()
        self.final_grade = final_grade
        db.session.commit()

    def calculate_final_grade(self):
        assessments: List[Assessment] = (
            self.get_student_situation_assessments()
        )
        total_weighting = self.calculate_total_weighting_in_section(
            assessments
        )
        sum_ponderates_grades = 0.0
        for assessment in assessments:
            final_grade_of_assessment = (
                self.calculate_user_grade_in_assessment(assessment)
            )
            sum_ponderates_grades += (
                final_grade_of_assessment
                * assessment.get_assessment_weighting()
            )
            if final_grade_of_assessment == 0.0:
                total_weighting -= assessment.weighting
        final_grade = sum_ponderates_grades / total_weighting
        return final_grade

    def calculate_total_weighting_in_section(self, assessments):
        total_weighting = sum(
            assessment.weighting for assessment in assessments
        )
        return total_weighting

    def _is_corresponding_task(self, grade, task):
        return grade.task_id == task.id

    def calculate_user_grade_in_assessment(self, assessment):
        tasks: List[Task] = self.get_assessment_tasks(assessment)
        grades: List[Grade] = self.get_user_grades_in_asessment(assessment)
        total_weighting = 0
        sum_ponderates_grades = 0.0
        for grade in grades:
            for task in tasks:
                if self._is_corresponding_task(grade, task):
                    if task.is_optional() and grade.get_score() is None:
                        continue
                    elif not task.is_optional() and grade.get_score() is None:
                        grade.set_default_score()
                    total_weighting += task.get_weighting()
                    sum_ponderates_grades += (
                        grade.get_score() * task.get_weighting()
                    )

        if total_weighting == 0:
            total_weighting = 1.0
        final_grade_of_assessment = sum_ponderates_grades / total_weighting
        return final_grade_of_assessment

    def get_user_situation_grades_in_asessment(self, assessment):
        grades = []
        for task in assessment.tasks:
            grade = Grade.get_grade_by_student_id_and_task_id(
                self.student_id, task.id
            )
            if grade:
                grades.append(grade)
        return grades
