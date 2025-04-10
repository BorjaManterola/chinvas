from flask import Blueprint

def register_routes(app):
    from app.routes.home_routes import home_bp
    from app.routes.user_routes import user_bp
    from app.routes.course_routes import course_bp
    from app.routes.period_routes import period_bp
    from app.routes.section_routes import section_bp
    from app.routes.prerequisite_routes import prerequisite_bp
    from app.routes.usersituation_routes import usersituation_bp
    from app.routes.group_routes import group_bp
    from app.routes.member_routes import member_bp
    from app.routes.assessment_routes import assessment_bp
    from app.routes.task_routes import task_bp
    from app.routes.grade_routes import grade_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(period_bp)
    app.register_blueprint(section_bp)
    app.register_blueprint(prerequisite_bp)
    app.register_blueprint(usersituation_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(grade_bp)