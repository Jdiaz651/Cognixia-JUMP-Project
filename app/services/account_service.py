# services/account_service.py
from app.models.Account import SavingsAccount, CheckingAccount
from app.services.customer_service import CustomerNotFound


class AccountNotFound(Exception):
    pass


def create(bank, owner_id, account_type, balance=0.0):
    owner = bank.find_customer(owner_id)
    if owner is None:
        raise CustomerNotFound(owner_id)

    if account_type == "checking":
        account = CheckingAccount(owner_id=owner_id, balance=balance)
    elif account_type == "savings":
        account = SavingsAccount(owner_id=owner_id, balance=balance)
    else:
        raise ValueError(f"Unknown account type: {account_type}")

    owner.add_account(account)
    return account


def get(bank, account_number):
    account = bank.find_account(account_number)
    if account is None:
        raise AccountNotFound(account_number)
    return account


def list_all(bank):
    accounts = []
    for customer in bank.customers:
        accounts.extend(customer.accounts)
    return accounts