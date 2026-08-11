# services/customer_service.py
from app.models.Customer import Customer


class CustomerNotFound(Exception):
    pass


def create(bank, name, email, branch_id):
    customer = Customer(bank.next_customer_id(), name, email, branch_id)
    bank.add_customer(customer)
    return customer


def list_all(bank):
    return bank.customers


def get(bank, customer_id):
    customer = bank.find_customer(customer_id)
    if customer is None:
        raise CustomerNotFound(customer_id)
    return customer


def update(bank, customer_id, name=None, email=None):
    customer = get(bank, customer_id)
    if name is not None:
        customer.name = name
    if email is not None:
        customer.email = email
    return customer


def deactivate(bank, customer_id):
    customer = get(bank, customer_id)
    customer.is_active = False
    return customer

def __str__(self):
    status = "active" if self.is_active else "inactive"
    return f"Customer #{self.id}: {self.name} ({self.email}), branch: {self.branch_id} [{status}]"