import os
import json
import pymysql

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

print(f"Connecting to database {DB_NAME} at {DB_HOST} with user {DB_USER}")

DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}

def loadJson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insertData(cursor, query, data):
    cursor.execute(query, data)
    
def populateStudents(cursor):
    students = loadJson('db/population/1-alumnos.json')['alumnos']
    for student in students:
        query = """
        INSERT INTO students (id, name, email, entry_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (student['id'], student['nombre'], student['correo'], f"{student['anio_ingreso']}-01-01")
        insertData(cursor, query, data)

def populateProfessors(cursor):
    professors = loadJson('db/population/2-profesores.json')['profesores']
    for professor in professors:
        query = """
        INSERT INTO teachers (id, name, email)
        VALUES (%s, %s, %s)
        """
        data = (professor['id'], professor['nombre'], professor['correo'])
        insertData(cursor, query, data)
        
def populatePrerequisites(cursor, course):
    for prereq_code in course['requisitos']:
        prereq_query = """
        INSERT INTO prerequisites (course_id, prerequisite_id)
        SELECT %s, id FROM courses WHERE code = %s
        """
        prereq_data = (course['id'], prereq_code)
        
        insertData(cursor, prereq_query, prereq_data)

def populateCourses(cursor):
    courses = loadJson('db/population/3-cursos.json')['cursos']
    for course in courses:
        query = """
        INSERT INTO courses (id, name, code, credits)
        VALUES (%s, %s, %s, %s)
        """
        data = (course['id'], course['descripcion'], course['codigo'], course['creditos'])
        insertData(cursor, query, data)
        
        print("Populating prerequisites for course:", course['id'])
        populatePrerequisites(cursor, course)

def populateCourseInstances(cursor):
    year = loadJson('db/population/4-instancias_cursos.json')['año']
    semester = loadJson('db/population/4-instancias_cursos.json')['semestre']
    instances = loadJson('db/population/4-instancias_cursos.json')['instancias']
    for instance in instances:
        query = """
        INSERT INTO periods (id, course_id, year, semester)
        VALUES (%s, %s, %s, %s)
        """
        data = (instance['id'], instance['curso_id'], year, semester)
        insertData(cursor, query, data)
        
def typeEvaluate(type):
    if type == 'peso':
        return 'Weight'
    elif type == 'porcentaje':
        return 'Percentage'
        
def populateTasks(cursor, task, assessment_id):
    for i in range(task["cantidad"]):
        task_query = """
        INSERT INTO tasks (assessment_id, optional, weighting)
        VALUES (%s, %s, %s)
        """
        task_data = (assessment_id, task['obligatorias'][i], task['valores'][i])
        insertData(cursor, task_query, task_data)
        
def populateAssessments(cursor, assessments, section):
    for assessment in assessments:
        assessment_query = """
        INSERT INTO assessments (id, section_id, name, type_evaluate, weighting)
        VALUES (%s, %s, %s, %s, %s)
        """
        type_evaluate_assessment = section['evaluacion']['topicos'][f"{assessment['id']}"]["tipo"]
        
        assessment_data = (assessment["id"], section['id'], assessment['nombre'],
                            typeEvaluate(type_evaluate_assessment), assessment['valor'])
        
        insertData(cursor, assessment_query, assessment_data)
        
        task=section['evaluacion']['topicos'][f"{assessment['id']}"]

        print("Populating tasks for assessment:", assessment['id'])
        populateTasks(cursor, task, assessment['id'])

def populateSections(cursor):
    sections = loadJson('db/population/5-instancia_cursos_con_secciones.json')['secciones']
    for section in sections:
        query = """
        INSERT INTO sections (id, period_id, teacher_id, type_evaluate)
        VALUES (%s, %s, %s, %s)
        """
        data = (section['id'], section['instancia_curso'], section["profesor_id"], typeEvaluate(section['evaluacion']['tipo']))
        insertData(cursor, query, data)
        
        assessments = section['evaluacion']['combinacion_topicos']
        
        print("Populating assessments for section:", section['id'])
        populateAssessments(cursor, assessments, section)
                
def populateStudentsPerSection(cursor):
    students_sections = loadJson('db/population/6-alumnos_por_seccion.json')['alumnos_seccion']
    for record in students_sections:
        query = """
        INSERT INTO student_situations (student_id, section_id, final_grade)
        VALUES (%s, %s, NULL)
        """
        data = (record['alumno_id'], record['seccion_id'])
        insertData(cursor, query, data)
        
def getTaskId(cursor, topic_id, instance, nota):
    task_query = """
    SELECT id FROM tasks
    WHERE assessment_id = %s
    ORDER BY id ASC
    LIMIT 1 OFFSET %s
    """
    offset = instance - 1
    cursor.execute(task_query, (topic_id, offset))
    result = cursor.fetchone()
    
    if result:
        print(f"Se encontró task_id {result[0]} para topico_id {topic_id} con instancia {instance}, nota {nota}")
        return result[0]
    else:
        print(f"No se encontró un task_id para topico_id {topic_id} con instancia {instance}")
        return None

def populateGrades(cursor):
    grades = loadJson('db/population/7-notas_alumnos.json')['notas']
    for grade in grades:
        
        task_id = getTaskId(cursor, grade['topico_id'], grade['instancia'], grade['nota'])

        if task_id:
            query = """
            INSERT INTO grades (student_id, task_id, score)
            VALUES (%s, %s, %s)
            """
            data = (grade['alumno_id'], task_id, grade['nota'])
            print(f"Data: {data}")
            insertData(cursor, query, data)

def populateClassrooms(cursor):
    classrooms = loadJson('db/population/8-salas_de_clases.json')['salas']
    for classroom in classrooms:
        query = """
        INSERT INTO classroom (id, name, capacity)
        VALUES (%s, %s, %s)
        """
        data = (classroom['id'], classroom['nombre'], classroom['capacidad'])
        insertData(cursor, query, data)

def main():
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        print("Populating Students...")
        populateStudents(cursor)
        print("Populating Professors...")
        populateProfessors(cursor)
        print("Populating Courses")
        populateCourses(cursor)
        print("Populating Course Instances...")
        populateCourseInstances(cursor)
        print("Populating Sections...")
        populateSections(cursor)
        print("Populating Students per Section...")
        populateStudentsPerSection(cursor)
        print("Populating Grades...")
        populateGrades(cursor)
        print("Populating Classrooms...")
        populateClassrooms(cursor)

        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main()