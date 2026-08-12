class Bank:
    def __init__(self):
        self.customers = []
        self.branches = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_branch(self, branch):
        self.branches.append(branch)

    def next_customer_id(self):
        return len(self.customers) + 1

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None

    def find_account(self, account_number):
        for customer in self.customers:
            for account in customer.accounts:
                if account.account_number == account_number:
                    return account
        return None

    def accounts_by_branch(self, branch_id):
        accounts = []
        for customer in self.customers:
            if customer.branch_id == branch_id:
                accounts.extend(customer.accounts)
        return accounts

    def transaction_volume_by_branch_month(self, branch_id, year, month):
        total = 0.0
        for account in self.accounts_by_branch(branch_id):
            for t in account.transactions:
                if t.timestamp.year == year and t.timestamp.month == month:
                    total += t.amount
        return total

    def branches_over_staff_ratio(self, max_ratio):
        result = []
        for branch in self.branches:
            ratio = len(branch.staff)
            if ratio > max_ratio:
                result.append(branch)
        return result