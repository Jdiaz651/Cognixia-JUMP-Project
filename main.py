from classes.Account import Account
from classes.Customer import Customer

def choose_account(customer):
    """Helper: let the user pick which account to act on. Returns an Account or None."""
    if not customer.accounts:
        print("You have no accounts.")
        return None

    customer.print_accounts()
    choice = input("Select an account number (from the list above): ")

    index = int(choice) - 1
    if not (0 <= index <= len(customer.accounts)):
        print("Invalid selection.")
        print("Please enter a valid number.")
        return None
    else:
        return customer.accounts[index]


def main():
    print("Welcome to the bank")
    username = input("Please enter your username:")
    password = input("Please enter you password:")

    current_customer = Customer(username, password)

    while True:
        print("\nWhat would you like to do?")
        print("1. Create a new account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. View transaction history")
        print("5. View accounts")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Account name: ")
            account_type = input("Account type (checking/savings): ")
            new_account = Account(name, account_type)
            current_customer.add_account(new_account)
            print(f"Created account: {new_account}")

        elif choice == "2":
            account = choose_account(current_customer)
            if account:
                amount = float(input("Amount to deposit: "))
                account.deposit(amount)
                print(f"New balance: ${account.balance}")

        elif choice == "3":
            account = choose_account(current_customer)
            if account:
                amount = float(input("Amount to withdraw: "))
                account.withdraw(amount)
                print(f"New balance: ${account.balance}")


        elif choice == "4":
            account = choose_account(current_customer)
            if account:
                account.print_transaction_history()

        elif choice == "5":
            current_customer.print_accounts()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")



if __name__ == "__main__":
    main()