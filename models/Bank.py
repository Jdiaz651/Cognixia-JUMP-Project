# Bank.py
from collections import defaultdict

class Bank:
    def __init__(self):
        self.customers = []
        self.branches = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_branch(self, branch):
        self.branches.append(branch)

    def accounts_by_branch(self, branch_id):
        """Which accounts belong to a specific branch?"""
        accounts = []
        for customer in self.customers:
            if customer.branch_id == branch_id:
                accounts.extend(customer.accounts)
        return accounts

    def transaction_volume_by_branch_month(self, branch_id, year, month):
        """Total transaction volume for a branch per month."""
        total = 0.0
        for account in self.accounts_by_branch(branch_id):
            for t in account.transactions:
                if t.timestamp.year == year and t.timestamp.month == month:
                    total += t.amount
        return total

    def branches_over_staff_ratio(self, max_ratio):
        """Which branches have a staff-to-manager ratio over a specified limit?"""
        result = []
        for branch in self.branches:
            # each branch has exactly one manager, so ratio = staff count / 1
            ratio = len(branch.staff)
            if ratio > max_ratio:
                result.append(branch)
        return result