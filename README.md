# FastAPI Catapult 🚀
FastAPI Catapult is your ultimate launchpad for building modern, scalable, and lightning-fast web applications. Designed with developers in mind, this project combines the simplicity and power of FastAPI with robust PostgreSQL integration, ensuring you can catapult your ideas into production-ready applications with ease.
## Features 🚀
- **FastAPI**: High-performance web framework for APIs.
- **PostgreSQL**: Reliable, powerful, and feature-rich relational database.
- **SQLAlchemy ORM**: Database interaction using modern Python idioms.
- **Alembic**: Database schema migrations.
- **Docker**: Fully containerized setup for easy deployment and development.
- **Pydantic**: Data validation and serialization.
- **Uvicorn**: ASGI server for running FastAPI.
- **Environment Management**: Configurable `.env` support.
- **Logging**: Configured with rotation for both file and console outputs.

---

## Project Structure 📂
```plaintext
fastapi_postgresql/
├── Dockerfile          # Docker build file
├── docker-compose.yaml # Multi-service setup (web & db)
├── requirements.txt    # Python dependencies
├── run.sh              # Run the app with environment setup
├── .env                # Environment variables
├── alembic/            # Database migrations setup
├── app/                # Application code
│   ├── main.py         # Entry point (FastAPI app)
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic (CRUD)
│   └── __init__.py     # Package initialization
└── logs_all/           # Application logs
```

---

## Getting Started 🏁

### Prerequisites
Ensure you have the following tools installed:
- **Docker** and **Docker Compose**
- **Python 3.13** or later

### Clone the Repository
```bash
git clone https://github.com/your-repo/fastapi_postgresql.git
cd fastapi_postgresql
```

### Setup Environment Variables
Create a `.env` file in the project root:
```bash
POSTGRES_USER=admin
POSTGRES_PASSWORD=change_me
POSTGRES_DB=db
```

---

## Deployment

### Deploying with Docker
To run the application using Docker:

1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. Access the application at:
   ```
   http://localhost:8080
   ```

3. Logs are stored in the `logs_all/` directory.

### Local Development
Run the database in Docker and the FastAPI server locally:

1. Start the database:
   ```bash
   docker-compose up db
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Export environment variables and start the server:
   ```bash
   bash run.sh
   ```

---

## Database Migrations ⚙️
### Create a Migration
Use Alembic to generate a new migration script:
```bash
docker-compose exec web alembic revision --autogenerate -m "Add new changes"
```

### Apply Migrations
```bash
docker-compose exec web alembic upgrade head
```

---

## CRUD Service Example

### Base Service CRUD
This project includes a generic `BaseServiceCrud` class that streamlines CRUD operations on SQLAlchemy models with Pydantic schemas.

#### Example Implementation
You can view it in branch 'example'
We'll create an API to manage `Cats`.

#### Cat Model (SQLAlchemy):
Place in `app/models/cat.py`
```python
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer

__all__ = ("Cat",)

class Cat(BaseModel):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
```
Don't forget to place in `app/models/__init__.py`
```python 
from .cat import *
```


#### Cat Schema (Pydantic):
Place in `app/schemas/cat.py`
```python
from pydantic import BaseModel
from typing import Optional


__all__ = ("CatCreateSchema", "CatSchema")

class CatCreateSchema(BaseModel):
    id: Optional[int]
    name: str
    age: int

class CatSchema(CatCreateSchema):
    id: int

    class Config:
        orm_mode = True
```

Don't forget to place in `app/schemas/__init__.py`
```python 
from .cat import *
```

#### Cat Service:
```python
from app.services.base_service_crud import BaseServiceCrud
from app.models import Cat
from app.schemas import CatCreate, CatRead

class CatService(BaseServiceCrud[Cat, CatRead, CatCreate]):
    def __init__(self, db):
        super().__init__(db, Cat, CatRead, CatCreate)
    
    @classmethod
    def _get_id(cls):
        return Cat.id
```

#### Cat Migration:
1. Generate the migration script:
   ```bash
   alembic revision --autogenerate -m "Add Cat model"
   ```

2. Apply the migration:
   ```bash
   alembic upgrade head
   ```

#### Endpoint for Cats:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db_dependency import get_db
from app.services.cat_service import CatService
from app.schemas.cat import CatCreate, CatRead

router = APIRouter()

@router.post("/cats", response_model=CatRead)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    service = CatService(db, Cat, CatRead, CatCreate)
    return service.create(cat)
```

---

## Verify the API
Check the API by visiting:
```plaintext
http://localhost:8080
```
Swagger UI for API testing is available at:
```plaintext
http://localhost:8080/docs
```

---

## Documentation

- Auto-generated API documentation is available at:
  - OpenAPI Docs: `/docs`
  - ReDoc: `/redoc`

- **File Structure:**
  - `app/` contains the application’s core logic.
  - `alembic/` manages database migrations.
  - `logs_all/` stores all log files.

---

## Dependencies 📦
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Alembic**: Migrations
- **Uvicorn**: ASGI server
- **PostgreSQL**: Database
- **Pydantic**: Validation

### Install Dependencies (Optional for Local Development)
```bash
pip install -r requirements.txt
```

---

## License 📜
This project is licensed under the MIT License.

## Contributing 🤝
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

Made with ❤️ to **start development faster**!

