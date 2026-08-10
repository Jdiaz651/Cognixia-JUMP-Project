from classes.Account import Account
class Customer():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self. accounts = []
        # default accounts every customer gets. mainly to test multiple accounts
        self.accounts.append(Account("test1","checking", 10.0))
        self.accounts.append(Account("test2","savings", 20.0))

    def add_account(self, account):
        self.accounts.append(account)

    def print_accounts(self):
        for i, acct in enumerate(self.accounts, start=1):
            print(f"{i}. {acct}")

    def __str__(self):
        return(self.username, self.password)
    