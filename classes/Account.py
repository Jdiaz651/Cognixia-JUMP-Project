class Account:
    def __init__(self, name, account_type, balance=0.0):
        self.name = name
        self.account_type = account_type
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive")
        else:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount:.2f}")
            
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive")
        elif amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount:.2f}")

    def print_transaction_history(self):
            if not self.transactions:
                print("No transactions yet.")
                return
            for t in self.transactions:
                print(t)        

    def __str__(self):
            return f"name: {self.name} type: {self.account_type} balance: {self.balance}"