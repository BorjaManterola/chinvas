import os
import json
import pymysql

from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv(dotenv_path="../.env")

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
DB_NAME = os.getenv('DB_NAME')

print(f"Connecting to database {DB_NAME} at {DB_HOST} with user {DB_USER}")

DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insert_data(cursor, query, data):
    cursor.execute(query, data)

def process_students(cursor):
    students = load_json('db/population/1-alumnos.json')['alumnos']
    for student in students:
        query = """
        INSERT INTO students (id, name, email, entry_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (student['id'], student['nombre'], student['correo'], f"{student['anio_ingreso']}-01-01")
        insert_data(cursor, query, data)

def process_professors(cursor):
    professors = load_json('db/population/2-profesores.json')['profesores']
    for professor in professors:
        query = """
        INSERT INTO teachers (id, name, email)
        VALUES (%s, %s, %s)
        """
        data = (professor['id'], professor['nombre'], professor['correo'])
        insert_data(cursor, query, data)

def process_courses(cursor):
    courses = load_json('db/population/3-cursos.json')['cursos']
    for course in courses:
        query = """
        INSERT INTO courses (id, name, code, credits)
        VALUES (%s, %s, %s, %s)
        """
        data = (course['id'], course['descripcion'], course['codigo'], course['creditos'])
        insert_data(cursor, query, data)

        for prereq_code in course['requisitos']:
            prereq_query = """
            INSERT INTO prerequisites (course_id, prerequisite_id)
            SELECT %s, id FROM courses WHERE code = %s
            """
            prereq_data = (course['id'], prereq_code)
            cursor.execute(prereq_query, prereq_data)

def process_course_instances(cursor):
    year = load_json('db/population/4-instancias_cursos.json')['año']
    semester = load_json('db/population/4-instancias_cursos.json')['semestre']
    instances = load_json('db/population/4-instancias_cursos.json')['instancias']
    for instance in instances:
        query = """
        INSERT INTO periods (id, course_id, year, semester)
        VALUES (%s, %s, %s, %s)
        """
        data = (instance['id'], instance['curso_id'], year, semester)
        insert_data(cursor, query, data)

def process_sections(cursor):
    sections = load_json('db/population/5-instancia_cursos_con_secciones.json')['secciones']
    for section in sections:
        query = """
        INSERT INTO sections (id, period_id, teacher_id, type_evaluate)
        VALUES (%s, %s, %s, %s)
        """
        data = (section['id'], section['instancia_curso'], section["profesor_id"], section['evaluacion']['tipo'])
        insert_data(cursor, query, data)
        
        assessments = section['evaluacion']['combinacion_topicos']
        tasks = section['evaluacion']['topicos']
        
        for assessment in assessments:
            assessment_query = """
            INSERT INTO assessments (id, section_id, name, type_evaluate, weighting)
            VALUES (%s, %s, %s, %s, %s)
            """
            type_evaluate_assessment = section['evaluacion']['topicos'][f"{assessment['id']}"]["tipo"]
            assessment_data = (assessment["id"], section['id'], assessment['nombre'],
                               type_evaluate_assessment, assessment['valor'])
            
            insert_data(cursor, assessment_query, assessment_data)
        
            task = tasks[f"{assessment['id']}"]
            
            for i in range(task["cantidad"]):
                task_query = """
                INSERT INTO tasks (assessment_id, optional, weighting)
                VALUES (%s, %s, %s)
                """
                task_data = (assessment["id"], task['obligatorias'][i], task['valores'][i])
                insert_data(cursor, task_query, task_data)
                

def process_students_per_section(cursor):
    students_sections = load_json('db/population/6-alumnos_por_seccion.json')['alumnos_seccion']
    for record in students_sections:
        query = """
        INSERT INTO student_situations (student_id, section_id, final_grade)
        VALUES (%s, %s, NULL)
        """
        data = (record['alumno_id'], record['seccion_id'])
        insert_data(cursor, query, data)

def process_grades(cursor):
    grades = load_json('db/population/7-notas_alumnos.json')['notas']
    for grade in grades:
        query = """
        INSERT INTO grades (student_id, task_id, score, feedback)
        VALUES (%s, %s, %s, NULL)
        """
        data = (grade['alumno_id'], grade['topico_id'], grade['nota'])
        insert_data(cursor, query, data)

def process_classrooms(cursor):
    classrooms = load_json('db/population/8-salas_de_clases.json')['salas']
    for classroom in classrooms:
        query = """
        INSERT INTO classroom (id, code, capacity)
        VALUES (%s, %s, %s)
        """
        data = (classroom['id'], classroom['nombre'], classroom['capacidad'])
        insert_data(cursor, query, data)

def main():
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        print("Processinf Students")
        process_students(cursor)
        print("Processing Professors")
        process_professors(cursor)
        print("Processing Courses")
        process_courses(cursor)
        print("Processing Course Instances")
        process_course_instances(cursor)
        print("Processing Sections")
        process_sections(cursor)
        print("Processing Students per Section")
        process_students_per_section(cursor)
        print("Processing Grades")
        process_grades(cursor)
        print("Processing Classrooms")
        process_classrooms(cursor)

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main()