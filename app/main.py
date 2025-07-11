"""
FastAPI application example.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
    Example root endpoint.
    :return: dict
    """
    return {"Hello": "World"}
