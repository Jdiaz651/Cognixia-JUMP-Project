from app.models.Account import Account, SavingsAccount, CheckingAccount
from app.models.Bank import Bank
from fake_data import load_fake_data
from datetime import datetime


def choose_customer(customers):
    print("\nAvailable customers (test data):")
    for i, cust in enumerate(customers, start=1):
        print(f"{i}. {cust}")

    choice = input("Select a customer number to log in as: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(customers):
            return customers[index]
        print("Invalid selection.")
        return None
    except ValueError:
        print("Please enter a valid number.")
        return None


def choose_account(customer):
    """Helper: let the user pick which account to act on. Returns an Account or None."""
    if not customer.accounts:
        print("You have no accounts.")
        return None

    customer.print_accounts()
    choice = input("Select an account number (from the list above): ")

    try:
        index = int(choice) - 1
        if 0 <= index < len(customer.accounts):
            return customer.accounts[index]
        print("Invalid selection.")
        return None
    except ValueError:
        print("Please enter a valid number.")
        return None


def get_amount(prompt):
    """Helper: safely read a positive float from the user."""
    try:
        return float(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None


def customer_menu(customer):
    while True:
        print(f"\n--- Logged in as {customer.name} ---")
        print("1. Create a new account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. View transaction history")
        print("5. View accounts")
        print("6. Log out")

        choice = input("Enter choice: ")

        if choice == "1":
            account_type = input("Account type (checking/savings): ").strip().lower()
            if account_type == "checking":
                new_account = CheckingAccount(owner_id=customer.id)
            elif account_type == "savings":
                new_account = SavingsAccount(owner_id=customer.id)
            else:
                print("Unknown account type.")
                continue
            customer.add_account(new_account)
            print(f"Created account: {new_account}")

        elif choice == "2":
            account = choose_account(customer)
            if account:
                amount = get_amount("Amount to deposit: ")
                if amount is not None:
                    try:
                        account.deposit(amount)
                        print(f"New balance: ${account.balance:.2f}")
                    except ValueError as e:
                        print(f"Error: {e}")

        elif choice == "3":
            account = choose_account(customer)
            if account:
                amount = get_amount("Amount to withdraw: ")
                if amount is not None:
                    try:
                        account.withdraw(amount)
                        print(f"New balance: ${account.balance:.2f}")
                    except ValueError as e:
                        print(f"Error: {e}")

        elif choice == "4":
            account = choose_account(customer)
            if account:
                account.print_transaction_history()

        elif choice == "5":
            customer.print_accounts()

        elif choice == "6":
            print("Logged out.")
            break

        else:
            print("Invalid choice, try again.")


def admin_menu(bank):
    """Exercises the Step 3 business logic questions on the fake data."""
    while True:
        print("\n--- Bank Admin / Reports ---")
        print("1. Accounts by branch")
        print("2. Transaction volume by branch (this month)")
        print("3. Branches over a staff ratio limit")
        print("4. Back to customer login")

        choice = input("Enter choice: ")

        if choice == "1":
            branch_id = input("Branch code (e.g. B1): ")
            accounts = bank.accounts_by_branch(branch_id)
            if not accounts:
                print("No accounts found for that branch.")
            for acct in accounts:
                print(acct)

        elif choice == "2":
            branch_id = input("Branch code (e.g. B1): ")
            now = datetime.now()
            total = bank.transaction_volume_by_branch_month(branch_id, now.year, now.month)
            print(f"Total transaction volume for {branch_id} this month: ${total:.2f}")

        elif choice == "3":
            limit = get_amount("Max staff ratio: ")
            if limit is not None:
                over = bank.branches_over_staff_ratio(limit)
                if not over:
                    print("No branches exceed that ratio.")
                for b in over:
                    print(b)

        elif choice == "4":
            break

        else:
            print("Invalid choice, try again.")


def main():
    print("Welcome to the bank")

    branches, customers = load_fake_data()
    bank = Bank()
    for b in branches:
        bank.add_branch(b)
    for c in customers:
        bank.add_customer(c)

    while True:
        print("\n1. Log in as a customer")
        print("2. Bank admin / reports")
        print("3. Exit")
        top_choice = input("Enter choice: ")

        if top_choice == "1":
            customer = choose_customer(customers)
            if customer:
                customer_menu(customer)

        elif top_choice == "2":
            admin_menu(bank)

        elif top_choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()