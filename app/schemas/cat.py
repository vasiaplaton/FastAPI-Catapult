"""
Cat schemas for creating and retrieving cat data.
"""
from typing import Optional
from pydantic import BaseModel

__all__ = ("CatCreateSchema", "CatSchema")


class CatCreateSchema(BaseModel):
    """
    Schema for creating a new cat.
    """
    id: Optional[int] = None
    name: str
    age: int


class CatSchema(CatCreateSchema):
    """
    Schema for retrieving cat data, including the ID.
    """
    id: int
