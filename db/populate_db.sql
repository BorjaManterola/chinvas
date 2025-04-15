-- Usuarios (profesores y alumnos)
INSERT INTO users (name, email, role, entry_date)
VALUES 
('Camila López', 'camila@uni.cl', 'profesor', NULL),
('Ignacio Rojas', 'nacho@uni.cl', 'alumno', '2022-03-01'),
('Sofía Morales', 'sofia@uni.cl', 'alumno', '2021-03-01'),
('Daniela Silva', 'dani@uni.cl', 'alumno', '2023-03-01');

-- Cursos
INSERT INTO courses (name, description)
VALUES 
('Diseño de Software Verificable', 'Curso ICC5130 sobre diseño y especificación.'),
('Estructura de Datos', 'Curso ICC213 sobre estructuras de datos.'),
('Bases de Datos', 'Curso ICC382 sobre diseño y uso de bases de datos.');

-- Periodos (instancias del curso)
INSERT INTO periods (course_id, nrc, semester)
VALUES 
(1, 10123, '2025-01'),
(2, 10124, '2025-01'),
(3, 10125, '2025-01');

-- Secciones
INSERT INTO sections (period_id, code, type_evaluate)
VALUES 
(1, 1, 'porcentaje'),
(2, 1, 'porcentaje'),
(3, 1, 'peso');

-- Prerrequisitos
INSERT INTO prerequisites (period_id, prerequisite_id)
VALUES 
(1, 2),  -- Diseño de Software requiere Estructura de Datos
(3, 2);  -- Bases de Datos también requiere Estructura de Datos

-- Situaciones de alumnos en secciones
INSERT INTO usersituations (user_id, section_id, situation, final_grade)
VALUES 
(2, 1, 'regular', NULL),
(3, 1, 'regular', NULL),
(4, 1, 'retirado', NULL);

-- Grupos
INSERT INTO groups (section_id, name)
VALUES 
(1, 'Grupo A'),
(1, 'Grupo B');

-- Miembros de grupo
INSERT INTO members (group_id, user_id)
VALUES 
(1, 2),
(1, 3),
(2, 4);

-- Evaluaciones
INSERT INTO assessments (section_id, name, type_evaluate, weighting)
VALUES 
(1, 'Controles', 'porcentaje', 40),
(1, 'Tareas', 'porcentaje', 60);

-- Tareas dentro de las evaluaciones
INSERT INTO tasks (assessment_id, name, optional, weighting, date)
VALUES 
(1, 'Control 1', 0, 50, '2025-04-01'),
(1, 'Control 2', 1, 50, '2025-04-08'),
(2, 'Tarea 1', 0, 100, '2025-04-10');

-- Notas de tareas
INSERT INTO grades (user_id, task_id, score, feedback)
VALUES 
(2, 1, 5.5, 'Buen trabajo'),
(2, 2, 6.0, 'Excelente'),
(2, 3, 4.0, 'Falta mejorar'),
(3, 1, 4.5, 'OK'),
(3, 2, NULL, 'No se presentó'),
(3, 3, 5.0, 'Bien');
