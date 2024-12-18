from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db_dependency import get_db
from app.services.cat_service import CatService
from app.schemas.cat import CatSchema, CatCreateSchema

app = FastAPI()


@app.post("/cats", response_model=CatSchema)
def create_cat(cat: CatCreateSchema, db: Session = Depends(get_db)):
    """
    Create a new cat in the database.
    """
    service = CatService(db)
    return service.create(cat)


@app.get("/cats/{cat_id}", response_model=CatSchema)
def get_cat_by_id(cat_id: int, db: Session = Depends(get_db)):
    """
    Get a single cat by its ID.
    """
    service = CatService(db)
    cat = service.get_by_id(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@app.get("/cats", response_model=list[CatSchema])
def get_all_cats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of cats with pagination.
    """
    service = CatService(db)
    cats = service.get_all()[skip: skip + limit]
    return cats