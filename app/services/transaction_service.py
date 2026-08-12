from app.models.Transaction import Transaction
from app.services.account_service import AccountNotFound


def transfer(bank, from_account_number, to_account_number, amount):
    from_acct = bank.find_account(from_account_number)
    to_acct = bank.find_account(to_account_number)

    if from_acct is None:
        raise AccountNotFound(from_account_number)
    if to_acct is None:
        raise AccountNotFound(to_account_number)

    from_acct.withdraw(amount)
    from_acct.transactions.pop()  # discard the auto-logged "Withdrawal"

    to_acct.balance += amount

    txn = Transaction(from_account_number, to_account_number, amount, "Transfer")
    from_acct.transactions.append(txn)
    to_acct.transactions.append(txn)

    return txn


def list_all(bank, start_date=None, end_date=None, type=None):
    seen_ids = set()
    unique_txns = []
    for customer in bank.customers:
        for account in customer.accounts:
            for txn in account.transactions:
                if txn.id not in seen_ids:
                    seen_ids.add(txn.id)
                    unique_txns.append(txn)

    if start_date is not None:
        unique_txns = [t for t in unique_txns if t.timestamp.date() >= start_date]
    if end_date is not None:
        unique_txns = [t for t in unique_txns if t.timestamp.date() <= end_date]
    if type is not None:
        unique_txns = [t for t in unique_txns if t.type.lower() == type.lower()]

    return sorted(unique_txns, key=lambda t: t.timestamp)