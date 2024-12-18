from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer

__all__ = ("Cat",)


class Cat(BaseModel):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
