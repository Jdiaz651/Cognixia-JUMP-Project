import itertools
from app.models.Transaction import Transaction


class Account:
    _account_number_counter = itertools.count(10000000)

    def __init__(self, owner_id, balance=0.0):
        self.account_number = next(Account._account_number_counter)
        self.owner_id = owner_id
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(
            Transaction(None, self.account_number, amount, "Deposit")
        )

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(
            Transaction(self.account_number, None, amount, "Withdrawal")
        )

    def get_balance(self):
        return self.balance

    def print_transaction_history(self):
        if not self.transactions:
            print("No transactions yet.")
            return
        for t in self.transactions:
            print(t)

    def __str__(self):
        return f"#{self.account_number} ({self.__class__.__name__}) - balance: ${self.balance:.2f}"


class SavingsAccount(Account):
    def __init__(self, owner_id, balance=0.0, minimum_balance=100.0):
        super().__init__(owner_id, balance)
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < self.minimum_balance:
            raise ValueError(
                f"Withdrawal would go below minimum balance of ${self.minimum_balance:.2f}"
            )
        self.balance -= amount
        self.transactions.append(
            Transaction(self.account_number, None, amount, "Withdrawal")
        )


class CheckingAccount(Account):
    def __init__(self, owner_id, balance=0.0, overdraft_limit=200.0):
        super().__init__(owner_id, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < -self.overdraft_limit:
            raise ValueError(
                f"Withdrawal exceeds overdraft limit of ${self.overdraft_limit:.2f}"
            )
        self.balance -= amount
        self.transactions.append(
            Transaction(self.account_number, None, amount, "Withdrawal")
        )