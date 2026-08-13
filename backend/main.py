from fastapi import FastAPI
from backend.controllers import customers, accounts, transactions


app = FastAPI(title="Bank API")

app.include_router(customers.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Bank API is running. See /docs for interactive docs."}