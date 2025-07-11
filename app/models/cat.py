"""
Cat model definition for the application.
"""
from sqlalchemy import Column, String, Integer
from app.models.base_model import BaseModel

__all__ = ("Cat",)


class Cat(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Represents a cat entity in the database.
    """
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
