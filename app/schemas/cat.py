from pydantic import BaseModel
from typing import Optional

__all__ = ("CatCreateSchema", "CatSchema")


class CatCreateSchema(BaseModel):
    id: Optional[int] = None
    name: str
    age: int


class CatSchema(CatCreateSchema):
    id: int
