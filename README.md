# StudyBud

StudyBud is a Django-based discussion platform where users can create topic-based rooms, post messages, and interact with other participants.

## Features

- Custom user model with email-based authentication
- User registration, login, logout, and profile update
- Create, update, and delete rooms
- Post and delete room messages
- Topic filtering and activity feed
- Basic REST API for rooms (`/api/rooms/`, `/api/rooms/<id>/`)

## Tech Stack

- Python
- Django
- Django REST Framework
- MySQL

## Project Structure

- `studybud/` - project settings and root URL config
- `base/` - main app (models, views, forms, templates, API)
- `templates/` - shared templates
- `static/` - CSS, JS, images

## Run the Project

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd studybud
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `mysqlclient` fails on your machine, add this optional fallback in `studybud/__init__.py`:

```python (optional):
import pymysql
pymysql.install_as_MySQLdb()
```

### 4. Configure MySQL

Create a MySQL database (example):

```sql
CREATE DATABASE studybud;
```

Update DB credentials in `studybud/settings.py` if needed:

- `NAME`
- `USER`
- `PASSWORD`
- `HOST`
- `PORT`

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

Admin: `http://127.0.0.1:8000/admin/`

## API Endpoints

- `GET /api/`
- `GET /api/rooms/`
- `GET /api/rooms/<id>/`

## Notes

- The project uses a custom user model (`base.User`) with `email` as `USERNAME_FIELD`.
- Ensure MySQL is running before starting the Django server.
