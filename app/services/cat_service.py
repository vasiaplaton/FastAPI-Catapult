from app.services.base_service_crud import BaseServiceCrud
from app.models import Cat
from app.schemas import CatSchema, CatCreateSchema


__all__ = ('CatService', )


class CatService(BaseServiceCrud[Cat, CatSchema, CatCreateSchema]):
    def __init__(self, db):
        super().__init__(db, Cat, CatSchema, CatCreateSchema)

    @classmethod
    def _get_id(cls):
        return Cat.id
