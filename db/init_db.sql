-- Elimina tablas si existen (respetando el orden de FK)
DROP TABLE IF EXISTS class, classroom, grades, tasks, assessments, members, `groups`,
    studentsituations, teachersections, prerequisites, sections, periods,
    courses, students, teachers;

CREATE TABLE teachers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    entry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    credits INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE classroom (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE periods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    year INT NOT NULL,
    semester VARCHAR(10),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE sections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    period_id INT NOT NULL,
    teacher_id INT NOT NULL,
    type_evaluate VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (period_id) REFERENCES periods(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE class (
    id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    classroom_id INT NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (classroom_id) REFERENCES classroom(id)
);

CREATE TABLE prerequisites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    prerequisite_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (prerequisite_id) REFERENCES courses(id)
);

CREATE TABLE student_situations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    final_grade DECIMAL(2,1),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

CREATE TABLE `groups` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

CREATE TABLE members (
    group_id INT,
    student_id INT,
    PRIMARY KEY (group_id, student_id),
    FOREIGN KEY (group_id) REFERENCES `groups`(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(255),
    type_evaluate VARCHAR(50),
    weighting FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    assessment_id INT NOT NULL,
    optional BOOLEAN,
    weighting FLOAT,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id)
);

CREATE TABLE grades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    task_id INT NOT NULL,
    score DECIMAL(5,2),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);