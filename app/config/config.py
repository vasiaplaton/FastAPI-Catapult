"""
Module for application configuration settings.
"""
from pydantic_settings import BaseSettings


class FileSettings(BaseSettings):
    """Класс, где храним переменные среды"""
    database_url: str


file_settings = FileSettings()
