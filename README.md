# Tutorial API

A robust, extensible Django REST API for managing programming tutorials, quizzes, and interview questions. This project supports multiple programming languages and integrates with Cloudinary for media management.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Seeding Data](#seeding-data)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Tutorial API** is designed to serve as a backend for educational platforms, providing structured content for tutorials, quizzes, and interview preparation. It supports rich media, hierarchical content organization, and is easily extensible for new languages or content types.

---

## Features

- **Tutorial Management:** Organize tutorials by categories, courses, sections, and lessons.
- **Quiz System:** Create quizzes with questions and multiple-choice options.
- **Interview Questions:** Store and serve interview questions and answers.
- **Cloudinary Integration:** Manage images and media assets efficiently.
- **Admin Interface:** Powerful Django admin for content management.
- **RESTful API:** Built with Django REST Framework for easy integration.
- **Filtering & Pagination:** Advanced filtering and optional pagination.
- **Permissions:** Custom permission classes for admin/read-only access.
- **Data Seeding:** Management commands for populating the database with sample data.

---

## Architecture

- **Django** as the backend framework.
- **Django REST Framework** for API endpoints.
- **Cloudinary** for media storage.
- **PostgreSQL** (recommended) or SQLite for development.
- Modular apps: `src` (core), `quiz`, `interview_question`.

---

## Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- Cloudinary
- dj-database-url
- django-filter
- dotenv

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Chaos-19/tutorial_api.git
   cd tutorial_api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in the required values (see below).

---

## Environment Variables

Create a `.env` file in the project root with the following keys:

```
DEBUG=True
SECRET_KEY=your-django-secret
DATABASE_URL=postgres://user:password@localhost:5432/dbname
CLOUD_NAME=your-cloudinary-cloud
API_KEY=your-cloudinary-api-key
API_SECRET=your-cloudinary-api-secret
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

## Database Migrations

Apply migrations to set up the database schema:

```bash
python manage.py migrate
```

---

## Seeding Data

Seed the database with sample tutorials, quizzes, and interview questions:

```bash
python manage.py seed_db
python manage.py seed_quiz_db
python manage.py seed_interview_db
```

You can also seed for other languages (e.g., Java, Flutter) using their respective commands if available.

---

## Usage

- **Run the development server:**
  ```bash
  python manage.py runserver
  ```
- Access the API at `http://localhost:8000/`
- Access the admin panel at `http://localhost:8000/admin/`

---

## API Endpoints

The API exposes endpoints for:

- Tutorials, Categories, Courses, Sections, Lessons
- Quizzes, Questions, Options
- Interview Questions

Authentication is required for admin actions. See the browsable API or API documentation for details.

---

## Testing

Run tests using:

```bash
python manage.py test
```

---

## Deployment

- Configure production settings (set `DEBUG=False`, update `ALLOWED_HOSTS`, etc.).
- Use a production-ready database (e.g., PostgreSQL).
- Set up static/media file hosting (Cloudinary is used for images).
- Use a WSGI server (e.g., Gunicorn) and a reverse proxy (e.g., Nginx).

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write clear, concise commit messages.
4. Ensure all tests pass.
5. Submit a pull request with a detailed description.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
# Tutorial API

A robust, extensible Django REST API for managing programming tutorials, quizzes, and interview questions. This project leverages Django, Django REST Framework, Cloudinary for media storage, and supports advanced features like Markdown conversion and content categorization.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Usage](#usage)
- [Admin Interface](#admin-interface)
- [API Endpoints](#api-endpoints)
- [Seeding Data](#seeding-data)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Tutorial Management**: Organize tutorials into categories, courses, sections, and lessons.
- **Quiz System**: Create quizzes with questions and multiple-choice options.
- **Interview Questions**: Store and retrieve interview questions and answers.
- **Cloudinary Integration**: Store and manage images and media files in Cloudinary.
- **Markdown Conversion**: Convert HTML content to Markdown using AI and custom logic.
- **Admin Dashboard**: Powerful Django admin for managing all content.
- **RESTful API**: Expose all resources via a browsable REST API.
- **Filtering & Pagination**: Advanced filtering and optional pagination for API endpoints.
- **CORS Support**: Configurable CORS for secure cross-origin requests.

---

## Architecture

- **Django**: Main web framework.
- **Django REST Framework**: API layer.
- **Cloudinary**: Media storage and management.
- **PostgreSQL/SQLite**: Database (configurable).
- **Docker (optional)**: For containerized deployment.

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- pip
- [Cloudinary Account](https://cloudinary.com/)
- PostgreSQL (or use SQLite for development)
- Node.js (if using Node-based language detection)

### Clone the Repository

```bash
git clone https://github.com/yourusername/tutorial_api.git
cd tutorial_api
```

### Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

See [Environment Variables](#environment-variables) for details.

---

## Environment Variables

The project uses environment variables for configuration. Key variables include:

- `SECRET_KEY`: Django secret key.
- `DEBUG`: Set to `True` for development, `False` for production.
- `DATABASE_URL`: Database connection string.
- `CLOUD_NAME`, `API_KEY`, `API_SECRET`: Cloudinary credentials.
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins.

---

## Database Migrations

Apply migrations to set up the database schema:

```bash
python manage.py migrate
```

---

## Usage

### Running the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

### Accessing the Admin Interface

Visit `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

Create a superuser if you haven't:

```bash
python manage.py createsuperuser
```

---

## API Endpoints

- [Endpoints](Endpoints.md)

API authentication and permissions are managed via Django REST Framework.

---

## Seeding Data

The project includes management commands to seed the database with sample data:

- **Tutorials, Categories, Courses, Lessons**:
  ```bash
  python manage.py seed_db
  ```
- **Quizzes**:
  ```bash
  python manage.py seed_quiz_db
  ```
- **Interview Questions**:
  ```bash
  python manage.py seed_interview_db
  ```

Ensure the required asset files are present in the `example/` directory.

---

## Testing

Run tests using:

```bash
python manage.py test
```

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write clear, concise commit messages.
4. Ensure all tests pass.
5. Submit a pull request with a detailed description.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contact

For questions or support, please open an issue or contact the maintainer.

