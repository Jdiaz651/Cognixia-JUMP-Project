from app.models.Account import Account
class Customer:
    def __init__(self, customer_id, name, email, branch_id):
        self.is_active = True
        self.id = customer_id
        self.name = name
        self.email = email
        self.branch_id = branch_id
        self.accounts = []  # list of Account objects

    def add_account(self, account):
        self.accounts.append(account)

    def print_accounts(self):
        for i, acct in enumerate(self.accounts, start=1):
            print(f"{i}. {acct}")


    def __str__(self):
        return f"Customer #{self.id}: {self.name} ({self.email}), branch: {self.branch_id}"

    