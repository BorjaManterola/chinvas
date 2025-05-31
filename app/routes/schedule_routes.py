from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import joinedload

from app import db
from app.models.class_ import Class
from app.models.classroom import Classroom
from app.models.course import Course
from app.models.period import Period
from app.models.schedule import Schedule
from app.models.section import Section

schedule_bp = Blueprint("schedule_routes", __name__, url_prefix="/schedules")


@schedule_bp.route("/form", methods=["GET"])
def new_schedule_form():
    return render_template("schedules/form.html", schedule=None)


@schedule_bp.route("/", methods=["POST"])
def create_schedule():
    if request.is_json:
        data = request.get_json()
        year = data.get("year")
        semester = data.get("semester")
    else:
        year = request.form.get("year")
        semester = request.form.get("semester")

    schedule, error = Schedule.handle_schedule_creation(year, semester)

    if schedule:
        try:
            return schedule.export_schedule_to_excel()
        except Exception as e:
            flash(
                f"Schedule created, but Excel download failed: {str(e)}",
                "warning",
            )
            return redirect(url_for("schedule_routes.get_schedules"))
    else:
        flash(error, "danger")
        return render_template("schedules/form.html", schedule=None)


@schedule_bp.route("/", methods=["GET"])
def get_schedules():
    year = request.args.get("year", type=int)
    if year:
        schedules = Schedule.query.filter_by(year=year).all()
    else:
        schedules = Schedule.query.all()
    return render_template("schedules/index.html", schedules=schedules)


@schedule_bp.route("/<int:id>", methods=["GET"])
def show_schedule(id):
    schedule = Schedule.query.get_or_404(id)

    classes = (
        Class.query.join(Section, Class.section_id == Section.id)
        .join(Period, Section.period_id == Period.id)
        .join(Classroom, Class.classroom_id == Classroom.id)
        .options(
            joinedload(Class.section).joinedload(Section.teacher),
            joinedload(Class.classroom),
        )
        .filter(Class.schedule_id == id)
        .all()
    )
    return render_template(
        "schedules/show.html", schedule=schedule, classes=classes
    )


@schedule_bp.route("/<int:id>/delete", methods=["POST"])
def delete_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    return redirect(url_for("schedule_routes.get_schedules"))


@schedule_bp.route("/<int:id>/export")
def export_schedule_to_excel(id):
    # TODO: Cambiar nombre a alguna funcion
    schedule = Schedule.query.get_or_404(id)
    try:
        return schedule.export_schedule_to_excel() # Conflicto de nombre
    except Exception as e:
        flash(
            f"An error occurred while generating the Excel file: {str(e)}",
            "danger",
        )
        return redirect(url_for("schedule_routes.show_schedule", id=id))
