from flask import Blueprint

def register_routes(app):
    from app.routes.home_routes import home_bp
    from app.routes.teacher_routes import teacher_bp
    from app.routes.student_routes import student_bp
    from app.routes.course_routes import course_bp
    from app.routes.period_routes import period_bp
    from app.routes.section_routes import section_bp
    from app.routes.prerequisite_routes import prerequisite_bp
    from app.routes.assessment_routes import assessment_bp
    from app.routes.task_routes import task_bp
    from app.routes.grade_routes import grade_bp
    from app.routes.student_situation_routes import student_situation_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(period_bp)
    app.register_blueprint(section_bp)
    app.register_blueprint(prerequisite_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(grade_bp)
    app.register_blueprint(student_situation_bp)
