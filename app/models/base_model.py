"""
This module defines the BaseModel class, serving as a base for ORM models in the system.
"""
from sqlalchemy.orm import DeclarativeBase

__all__ = ('BaseModel',)


class BaseModel(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """
    A base model class for ORM models, providing utility methods to streamline attribute updates.
    """
    __abstract__ = True

    def update(self, **kwargs):
        """
        Updates the instance attributes with the provided keyword arguments.

        This method allows for selective updating of instance attributes, only setting the values of attributes
        that are already defined on the instance. If a specified attribute does not exist on the model instance,
        it will be ignored, ensuring that only valid attributes are updated. This is useful for handling partial
        updates on model instances.

        Parameters:
            **kwargs: Arbitrary keyword arguments where the key is the name of the attribute to update and
            the value is the new value to set for that attribute.

        Example:
            instance.update(attr1=value1, attr2=value2)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
