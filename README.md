# StudyMate AI

StudyMate AI is a backend platform for an AI-powered study and note-taking application.

The project is being developed as a scalable, production-oriented application that will eventually combine structured note management, speech-to-text, AI-powered summarization, retrieval-augmented generation (RAG), and agentic AI capabilities.

## Current Status

The backend foundation is currently implemented with:

* FastAPI REST API
* PostgreSQL database
* SQLAlchemy ORM
* Alembic database migrations
* JWT-based authentication
* Argon2 password hashing
* Protected API endpoints
* User-specific Notes CRUD
* Environment-based configuration

AI-powered capabilities are planned and will be added incrementally.

---

## Technology Stack

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic / Pydantic Settings

### Authentication & Security

* PyJWT
* HTTP Bearer authentication
* Argon2 password hashing
* Environment-based secrets

### Development

* Visual Studio Code
* Git
* GitHub

---

## Architecture

The current backend follows a layered structure:

```text
Client
  |
  v
FastAPI API
  |
  +------------------+
  |                  |
  v                  v
API / Routers      Dependencies
  |                  |
  v                  v
Services          Authentication
  |
  v
SQLAlchemy
  |
  v
PostgreSQL
```

Database schema changes are managed separately through Alembic migrations.

---

## Project Structure

```text
StudyMate-AI/
│
├── backend/
│   ├── .env
│   ├── .env.example
│   ├── alembic.ini
│   ├── requirements.txt
│   │
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │
│   └── app/
│       ├── main.py
│       ├── dependencies.py
│       │
│       ├── api/
│       │   ├── router.py
│       │   └── v1/
│       │       ├── auth.py
│       │       ├── notes.py
│       │       ├── health.py
│       │       └── protected.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   └── security.py
│       │
│       ├── database/
│       │   └── database.py
│       │
│       ├── models/
│       │   ├── user.py
│       │   └── note.py
│       │
│       ├── schemas/
│       │   ├── auth.py
│       │   └── note.py
│       │
│       ├── services/
│       │   ├── auth_service.py
│       │   └── note_service.py
│       │
│       └── utils/
│           └── jwt.py
│
├── docs/
├── frontend/
├── scripts/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Authentication Flow

StudyMate AI uses JWT-based authentication.

```text
User
  |
  | Email + Password
  v
POST /auth/login
  |
  v
User lookup in PostgreSQL
  |
  v
Argon2 password verification
  |
  v
JWT access token generated
  |
  v
Protected API requests
```

Passwords are never stored as plain text. Passwords are hashed using Argon2 before being stored in the database.

---

## Database

The application uses PostgreSQL as its primary database.

Current database entities include:

### Users

Stores application user information and authentication credentials.

### Notes

Stores notes belonging to individual users.

Each note is associated with a user through a foreign-key relationship.

Notes currently support:

* Title
* Content
* User ownership
* Created timestamp
* Updated timestamp

---

## Database Migrations

Alembic is used to manage database schema changes.

The current migration chain includes:

```text
Initial database schema
        |
        v
Add note timestamps
```

The database migration state can be checked with:

```bash
alembic current
```

New schema changes should be introduced through Alembic migrations rather than using SQLAlchemy `create_all()` in the application startup.

Typical migration workflow:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

---

## API Endpoints

### Authentication

```text
POST /auth/register
POST /auth/login
```

### Notes

```text
POST   /notes/
GET    /notes/
GET    /notes/{note_id}
PUT    /notes/{note_id}
DELETE /notes/{note_id}
```

### Protected APIs

Protected endpoints require a valid JWT access token using HTTP Bearer authentication.

---

## Environment Configuration

Sensitive configuration is stored in a local `.env` file.

Example configuration:

```env
DATABASE_URL=postgresql+psycopg://postgres:<password>@localhost:5432/studymate
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

Do not commit the actual `.env` file to Git.

The repository contains:

```text
backend/.env.example
```

as a configuration template.

---

## Running the Backend Locally

Navigate to the backend directory:

```bash
cd backend
```

Activate the project's Python virtual environment if it is not already active.

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Security

The current backend includes:

* JWT authentication
* HTTP Bearer authentication
* Argon2 password hashing
* Environment-based secrets
* User-level note ownership checks
* PostgreSQL database
* Alembic-controlled schema changes

Production deployment will require additional security hardening and infrastructure configuration.

---

## Roadmap

The following capabilities are planned for future versions.

### Speech-to-Text

Convert lectures, recordings, and other audio input into searchable text.

Planned direction:

```text
Audio
  |
  v
Speech-to-Text
  |
  v
Transcript
```

### AI Summarization

Generate structured summaries from notes and transcripts.

Potential outputs include:

* Short summaries
* Detailed summaries
* Key concepts
* Important points
* Action items

### Retrieval-Augmented Generation (RAG)

Allow users to ask questions against their own study material.

Planned architecture:

```text
Notes / Transcripts
        |
        v
Chunking
        |
        v
Embeddings
        |
        v
Vector Store
        |
        v
Retriever
        |
        v
LLM
        |
        v
Context-aware Answer
```

### AI Study Assistant

Future versions will introduce an AI assistant capable of working with a user's study material.

Potential capabilities include:

* Question answering
* Concept explanations
* Study notes generation
* Question generation
* Flashcards
* Revision assistance

### Agentic AI

The longer-term architecture may introduce specialized AI agents for tasks such as:

```text
Study Assistant
      |
      +-- Summarization
      |
      +-- Question Generation
      |
      +-- Flashcards
      |
      +-- Knowledge Retrieval
      |
      +-- Study Planning
```

These features will be documented as they are implemented and tested.

---

## Development Philosophy

StudyMate AI is being developed incrementally with emphasis on:

* Maintainable architecture
* Secure authentication
* Database reliability
* Clear separation of responsibilities
* Testability
* Scalable AI integration
* Production-oriented design

The backend foundation is being established before introducing the AI and agentic components so that future capabilities can be integrated without requiring major architectural rework.

---

## License

License information will be added as the project moves toward release.
