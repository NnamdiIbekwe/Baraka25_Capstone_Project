# Baraka25 Capstone Project

A Python-based web application for managing courses, enrollments, and user authentication. This project uses FastAPI, SQLAlchemy, and Alembic for backend development and database migrations.

## Features
- User registration and authentication
- Course management (CRUD)
- Enrollment management
- RESTful API endpoints
- Database migrations with Alembic
- Docker support for easy deployment
- Unit and integration tests

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- Docker & Docker Compose
- Pytest

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Docker & Docker Compose (optional, for containerized setup)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Baraka25_Capstone_Project.git
   cd Baraka25_Capstone_Project
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Migration
Run Alembic migrations to set up the database schema:
```bash
alembic upgrade head
```

### Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

Or use Docker Compose:
```bash
docker-compose up --build
```

### Running Tests
```bash
pytest
```

## API Documentation
Once the server is running, access the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing
This project for 3rd semester capstone exam project.
