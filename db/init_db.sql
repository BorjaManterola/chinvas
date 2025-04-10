-- Elimina tablas si existen (respetando el orden de FK)
DROP TABLE IF EXISTS grades, tasks, assessments, members, `groups`,
    usersituations, prerequisites, sections, periods,
    courses, users;

-- Tabla: users
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    entry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: courses
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: periods
CREATE TABLE periods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    nrc INT NOT NULL,
    semester VARCHAR(10),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Tabla: sections
CREATE TABLE sections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    period_id INT NOT NULL,
    code INT,
    type_evaluate VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (period_id) REFERENCES periods(id)
);

-- Tabla: prerequisites
CREATE TABLE prerequisites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    period_id INT NOT NULL,
    prerequisite_id INT NOT NULL,
    FOREIGN KEY (period_id) REFERENCES periods(id),
    FOREIGN KEY (prerequisite_id) REFERENCES courses(id)
);

-- Tabla: usersituations
CREATE TABLE usersituations (
    user_id INT,
    section_id INT,
    situation VARCHAR(50),
    final_grade DECIMAL(4,2),
    PRIMARY KEY (user_id, section_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

-- Tabla: groups
CREATE TABLE `groups` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

-- Tabla: members
CREATE TABLE members (
    group_id INT,
    user_id INT,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES `groups`(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabla: assessments
CREATE TABLE assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    section_id INT NOT NULL,
    name VARCHAR(255),
    type_evaluate VARCHAR(50),
    weighting INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id)
);

-- Tabla: tasks
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    assesstment_id INT NOT NULL,
    name VARCHAR(255),
    optional BOOLEAN,
    weighting INT,
    date DATE,
    FOREIGN KEY (assesstment_id) REFERENCES assessments(id)
);

-- Tabla: grades
CREATE TABLE grades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    score DECIMAL(5,2),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);