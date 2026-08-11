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
    
    def next_customer_id(self):
        return len(self.customers) + 1        
    
    def branches_over_staff_ratio(self, max_ratio):
        """Which branches have a staff-to-manager ratio over a specified limit?"""
        result = []
        for branch in self.branches:
            # each branch has exactly one manager, so ratio = staff count / 1
            ratio = len(branch.staff)
            if ratio > max_ratio:
                result.append(branch)
        return result