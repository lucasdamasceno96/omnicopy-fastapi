# FastAPI CRUD Hands-On

This is a simple hands-on project developed to keep Python and FastAPI skills sharp. It implements a basic CRUD (Create, Read, Update, Delete) API for managing marketing campaigns, following modern software development best practices.

The main goal is to practice and demonstrate:
- A clean, layered architecture (API, Services, Data Access).
- Dependency Injection in FastAPI.
- Data validation using Pydantic and SQLModel.
- Consistent development environments through containerization with Docker.

---

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM & Validation:** [SQLModel](https://sqlmodel.tiangolo.com/) (combining Pydantic and SQLAlchemy)
- **Database:** [SQLite](https://www.sqlite.org/index.html)
- **Web Server:** [Uvicorn](https://www.uvicorn.org/)
- **Containerization:** [Docker](https://www.docker.com/)

---

## Why SQLite?

SQLite was chosen for its simplicity and file-based nature, making it perfect for development, practice, and portability without requiring a separate database server. For a production environment, this could be easily swapped with a more robust database like PostgreSQL or MySQL by simply changing the database connection string in the `db/database.py` file.

---

## Project Structure

The project follows a layered architecture to ensure separation of concerns and maintainability.

```
.
├── db/                 # Data Access Layer (Engine, Session management)
├── models/             # Data Models and Schemas (Pydantic/SQLModel)
├── routers/            # API Layer (HTTP Endpoints)
├── services/           # Business Logic Layer
├── .gitignore          # Files to be ignored by Git
├── main.py             # Main application entrypoint
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

---

## How to Run

### 1. Running Locally (Recommended for Development)

**Prerequisites:** Python 3.9+

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <project-folder-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    *Navigate to the directory that contains the `omnicopy` folder* and run:
    ```bash
    uvicorn omnicopy.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. The interactive documentation (Swagger UI) will be at `http://127.0.0.1:8000/docs`.

### 2. Running with Docker

**Prerequisites:** Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t fastapi-campaigns-api .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -d -p 8000:8000 --name campaigns-api fastapi-campaigns-api
    ```
    The API will be available at `http://localhost:8000`. The interactive documentation will be at `http://localhost:8000/docs`.

---

## API Endpoints

The API provides the following endpoints for managing campaigns:

| Method | Path                  | Description                 |
|--------|-----------------------|-----------------------------|
| GET    | `/`                   | Shows a welcome message.    |
| GET    | `/campaigns`          | Retrieves a list of all campaigns. |
| GET    | `/campaigns/{id}`     | Retrieves a single campaign by ID. |
| POST   | `/campaigns`          | Creates a new campaign.     |
| PUT    | `/campaigns/{id}`     | Updates an existing campaign by ID. |
| DELETE | `/campaigns/{id}`     | Deletes a campaign by ID.   |