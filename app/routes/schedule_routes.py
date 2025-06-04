from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models.schedule import Schedule

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
            return schedule.export_to_excel()
        except Exception as e:
            flash(
                f"Schedule created, but Excel download failed: {str(e)}",
                "warning",
            )
            return redirect(url_for("schedule_routes.schedules_index"))
    else:
        flash(error, "danger")
        return render_template("schedules/form.html", schedule=None)


@schedule_bp.route("/", methods=["GET"])
def schedules_index():
    year = request.args.get("year", type=int)
    if year:
        schedules = Schedule.get_schedules_by_year(year)
    else:
        schedules = Schedule.get_all_schedules_sorted_by_year()
    return render_template("schedules/index.html", schedules=schedules)


@schedule_bp.route("/<int:id>", methods=["GET"])
def show_schedule(id):
    schedule = Schedule.get_schedule_by_id(id)

    classes = Schedule.get_classes_by_schedule_id(id)
    return render_template(
        "schedules/show.html", schedule=schedule, classes=classes
    )


@schedule_bp.route("/<int:id>/delete", methods=["POST"])
def delete_schedule(id):
    schedule = Schedule.get_schedule_by_id(id)
    db.session.delete(schedule)
    db.session.commit()
    return redirect(url_for("schedule_routes.schedules_index"))


@schedule_bp.route("/<int:id>/export")
def export_schedule_to_excel(id):
    schedule = Schedule.get_schedule_by_id(id)
    try:
        return schedule.export_to_excel()
    except Exception as e:
        flash(
            f"An error occurred while generating the Excel file: {str(e)}",
            "danger",
        )
        return redirect(url_for("schedule_routes.show_schedule", id=id))
