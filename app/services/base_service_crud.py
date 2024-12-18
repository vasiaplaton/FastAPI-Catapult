"""
Defines a generic base service class `BaseServiceCrud` for CRUD operations on SQLAlchemy models with Pydantic schemas.

The `BaseServiceCrud` class is a reusable base class for creating CRUD service layers in applications that use SQLAlchemy
for ORM models and Pydantic for data validation. It provides methods for creating, reading, updating, and deleting
database records, converting between SQLAlchemy models and Pydantic schemas. This design pattern allows for type safety
and easy schema validation when interacting with the database.
"""
from abc import abstractmethod
from typing import Type, Generic, TypeVar, Optional, Any

import pydantic
from sqlalchemy import Column
from sqlalchemy import select, update

from app.models.base_model import BaseModel

_all_ = ('BaseServiceCrud',)

# pylint: disable=invalid-name
ModelType = TypeVar('ModelType', bound=BaseModel)
# pylint: disable=invalid-name
SchemaType = TypeVar('SchemaType', bound=pydantic.BaseModel)
# pylint: disable=invalid-name
CreateSchemaType = TypeVar('CreateSchemaType', bound=pydantic.BaseModel)


class BaseServiceCrud(Generic[ModelType, SchemaType, CreateSchemaType]):
    """
    Base service class for CRUD operations on SQLAlchemy models with Pydantic schema validation.

    Attributes:
        db: The database session used for executing queries.
        model: The SQLAlchemy model type managed by this service.
        schema: The Pydantic schema type used for output validation.
        create_schema: The Pydantic schema type used for input validation when creating a new entity.
    """

    def __init__(self, db, model: Type[ModelType], schema: Type[SchemaType], create_schema: Type[CreateSchemaType]):
        self.db = db
        self.model = model
        self.schema = schema
        self.create_schema = create_schema

    def _on_creation(self, model: ModelType):
        """
        Hook method that can be overridden in subclasses to add additional processing upon creation.
        """

    @classmethod
    @abstractmethod
    def _get_id(cls) -> Type[Column]:
        """
        Returns the primary key column of the model.
        This method should be implemented by subclasses to specify the primary key column.
        """

    def from_model(self, m: ModelType) -> Optional[SchemaType]:
        """
        Converts a SQLAlchemy model instance to a Pydantic schema instance.

        Args:
            m (ModelType): The SQLAlchemy model instance.

        Returns:
            SchemaType: The corresponding Pydantic schema instance.
        """
        if not m:
            return None
        return self.schema.model_validate(m.__dict__)

    def to_model(self, s: SchemaType):
        """
        Converts a Pydantic schema instance to a SQLAlchemy model instance.

        Args:
            s (SchemaType): The Pydantic schema instance.

        Returns:
            ModelType: The corresponding SQLAlchemy model instance.
        """
        return self.model(**s.model_dump())

    def from_models(self, models_in: ModelType) -> list[SchemaType]:
        """
        Converts a list of SQLAlchemy model instances to a list of Pydantic schema instances.

        Args:
            models_in (list[ModelType]): The list of SQLAlchemy model instances.

        Returns:
            list[SchemaType]: A list of corresponding Pydantic schema instances.
        """
        return [self.from_model(m) for m in models_in]

    def get_by_id(self, id_in) -> Optional[SchemaType]:
        """
        Retrieves a single record by its primary key.

        Args:
            id_in: The primary key value.

        Returns:
            SchemaType: The retrieved record as a Pydantic schema instance, or None if not found.
        """
        query = select(self.model)
        query = query.filter(self._get_id() == id_in)
        return self.from_model((self.db.execute(query)).scalars().first())

    def create(self, schema: CreateSchemaType) -> SchemaType:
        """
        Creates a new record in the database.

        Args:
            schema (CreateSchemaType): The schema instance containing data for the new record.

        Returns:
            SchemaType: The created record as a Pydantic schema instance.
        """
        db_item = self.model(**schema.model_dump())
        self._on_creation(db_item)
        self.db.add(db_item)
        self.db.flush()

        return self.from_model(db_item)

    def update(self, id_in, schema: CreateSchemaType) -> None:
        """
        Updates an existing record in the database.

        Args:
            id_in: The primary key value of the record to update.
            schema (pydantic.BaseModel): The schema instance with updated data.

        """
        query = update(self.model)
        query = query.where(self._get_id() == id_in)
        query = query.values(**schema.model_dump(exclude_unset=True))

        self.db.execute(query)
        self.db.flush()

    def crupdate(self, id_in, schema: CreateSchemaType) -> None:
        if self.get_by_id(id_in):
            self.update(id_in, schema)
        else:
            self.create(schema)


    def delete(self, id_in) -> SchemaType:
        """
        Deletes a record by its primary key.

        Args:
            id_in: The primary key value of the record to delete.

        Returns:
            SchemaType: The deleted record as a Pydantic schema instance.
        """
        query = select(self.model)
        query = query.filter(self._get_id() == id_in)

        entity = self.db.execute(query).scalars().first()
        self.db.delete(entity)
        self.db.flush()

        return self.from_model(entity)

    def get_all(self) -> list[SchemaType]:
        """
        Retrieves all records of the model type.

        Returns:
            list[SchemaType]: A list of all records as Pydantic schema instances.
        """
        query = select(self.model)
        return self.from_models((self.db.execute(query)).scalars().all())

    def build_filter_query(self, kwargs: dict[str, Any]):
        query = select(self.model)
        for key, value in kwargs.items():
            attr = getattr(self.model, key)
            if not attr:
                raise AttributeError
            query = query.filter(getattr(self.model, key) == value)
        return query

    def find_all_by_filters(self, **kwargs):
        query = self.build_filter_query(kwargs)
        return self.execute_and_get_all(query)

    def find_one_by_filters(self, **kwargs):
        query = self.build_filter_query(kwargs)
        return self.execute_and_get_one(query)

    def execute_and_get_one(self, query) -> Optional[SchemaType]:
        return self.from_model((self.db.execute(query)).scalars().first())

    def execute_and_get_all(self, query) -> list[SchemaType]:
        return self.from_models((self.db.execute(query)).scalars().all())
