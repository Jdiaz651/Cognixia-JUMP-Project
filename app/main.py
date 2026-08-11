from fastapi import FastAPI
from app.controllers import customers, accounts, transactions
from app.store import bank
from app.fake_data import load_fake_data

app = FastAPI(title="Bank API")

_branches, _customers = load_fake_data()
for b in _branches:
    bank.add_branch(b)
for c in _customers:
    bank.add_customer(c)

app.include_router(customers.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Bank API is running. See /docs for interactive docs."}