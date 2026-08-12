from datetime import datetime
import itertools


class Transaction:
    _id_counter = itertools.count(1)

    def __init__(self, from_account, to_account, amount, transaction_type):
        self.id = next(Transaction._id_counter)
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.type = transaction_type
        self.timestamp = datetime.now()

    def __str__(self):
        return (
            f"#{self.id} [{self.type}] ${self.amount:.2f} "
            f"from:{self.from_account} to:{self.to_account} "
            f"at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )