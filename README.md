# Chinvas - Sistema de Gestión Académica

Este proyecto es una aplicación web desarrollada con Flask y MySQL para gestionar cursos, alumnos, profesores, evaluaciones y notas.

---

## 🚀 Requisitos

- Python 3.9 o superior
- MySQL 8.x
- pip
- Entorno virtual (`venv` recomendado)

---

## ⚙️ Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/BorjaManterola/Proyecto-DSV.git
cd chinvas
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

- En Windows:
```bash
.venv\Scripts\activate
```

- En Mac/Linux:
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🛢️ Configuración de base de datos

Se tienen que instalar mySQL y crearse una cuenta

🔧 [Haz clic aquí para descargar MySQL Installer](https://dev.mysql.com/downloads/installer/)

### 1. Crear la base de datos en MySQL

```sql
mysql -u root -p
CREATE DATABASE chinvas;
```

### 2. Crear archivo `.env` en la raíz del proyecto

```env
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_NAME=chinvas
```

> ⚠️ Si tu contraseña tiene símbolos especiales (como `@`, `:` o `/`), se manejarán automáticamente gracias al uso de `quote_plus`.

### 3. Ejecutar los scripts SQL

```bash
Get-Content db/init_db.sql | mysql -u root -p chinvas
Get-Content db/populate_db.sql | mysql -u root -p chinvas
```

---

## 🧪 Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en: http://localhost:5000

---

## 🧼 Salir del entorno virtual

```bash
deactivate
```

---

## 🤝 Recomendaciones para trabajo en grupo

- No subir el archivo `.env` al repositorio.
- Agregar `.env` a `.gitignore`.
- Compartir un archivo `.env.example` para que todos sepan cómo configurar el suyo.
- Usar `requirements.txt` actualizado para mantener las dependencias sincronizadas.

---

## 📁 Estructura del proyecto

```
chinvas/
├── app/
│   ├── models/
│   ├── routes/
│   └── __init__.py
├── db/
│   ├── init_db.sql
│   └── populate_db.sql
├── config.py
├── run.py
├── .env (no se sube)
├── requirements.txt
└── README.md
```

---

## 📌 Autores

- Equipo Chinvas 💻🎓
