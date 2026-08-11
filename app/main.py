# main.py
from fastapi import FastAPI
from app.controllers import customers

app = FastAPI(title="Bank API")

app.include_router(customers.router)


@app.get("/")
def root():
    return {"message": "Bank API is running. See /docs for interactive docs."}