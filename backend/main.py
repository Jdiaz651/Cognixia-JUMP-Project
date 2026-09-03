import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.controllers import customers, accounts, transactions

app = FastAPI(title="Bank API")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Bank API is running. See /docs for interactive docs."}
