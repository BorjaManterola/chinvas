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
        INSERT INTO courses (id, name, code, description)
        VALUES (%s, %s, %s, %s)
        """
        data = (course['id'], course['codigo'], course['descripcion'])
        insert_data(cursor, query, data)

def process_course_instances(cursor):
    instances = load_json('db/population/4-instancias_cursos.json')['instancias']
    for instance in instances:
        query = """
        INSERT INTO periods (id, course_id, semester)
        VALUES (%s, %s, '2025-1')
        """
        data = (instance['id'], instance['curso_id'])
        insert_data(cursor, query, data)

def process_sections(cursor):
    sections = load_json('db/population/5-instancia_cursos_con_secciones.json')['secciones']
    for section in sections:
        query = """
        INSERT INTO sections (id, period_id, nrc, type_evaluate)
        VALUES (%s, %s, %s, %s)
        """
        data = (section['id'], section['instancia_curso'], section['nrc'], section['evaluacion']['tipo'])
        insert_data(cursor, query, data)

def process_students_per_section(cursor):
    students_sections = load_json('db/population/6-alumnos_por_seccion.json')['alumnos_seccion']
    for record in students_sections:
        query = """
        INSERT INTO studentsituations (student_id, section_id, final_grade)
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