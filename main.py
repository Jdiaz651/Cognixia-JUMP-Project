from classes.Account import Account
def main():
    print("Welcome to the bank")
    username = input("Please enter your username:")
    password = input("Please enter you password:")

    current_account = Account(username, password)

    print(current_account)

if __name__ == "__main__":
    main()