from app.models.Branch import Branch
from app.models.Customer import Customer
from app.models.Account import SavingsAccount, CheckingAccount

def load_fake_data():
    """Builds sample branches, customers, and accounts (with transaction history) for testing."""

    # Branches
    downtown = Branch("B1", "Downtown", manager_id="M001")
    downtown.add_staff("S001")
    downtown.add_staff("S002")
    downtown.add_staff("S003")

    uptown = Branch("B2", "Uptown", manager_id="M002")
    uptown.add_staff("S004")

    branches = [downtown, uptown]

    # Customers
    alice = Customer(1, "Alice Johnson", "alice@email.com", branch_id="B1")
    bob = Customer(2, "Bob Nguyen", "bob@email.com", branch_id="B2")

    # Give Alice a checking + savings account with some starting activity
    alice_checking = CheckingAccount(owner_id=alice.id, balance=500.0, overdraft_limit=200.0)
    alice_checking.deposit(150.0)
    alice_checking.withdraw(75.0)

    alice_savings = SavingsAccount(owner_id=alice.id, balance=1000.0, minimum_balance=100.0)
    alice_savings.deposit(200.0)

    alice.add_account(alice_checking)
    alice.add_account(alice_savings)

    # Give Bob a checking + savings account too
    bob_checking = CheckingAccount(owner_id=bob.id, balance=300.0, overdraft_limit=100.0)
    bob_checking.withdraw(50.0)

    bob_savings = SavingsAccount(owner_id=bob.id, balance=250.0, minimum_balance=50.0)
    bob_savings.deposit(100.0)
    bob_savings.withdraw(30.0)

    bob.add_account(bob_checking)
    bob.add_account(bob_savings)

    customers = [alice, bob]

    return branches, customers