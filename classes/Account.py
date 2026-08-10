class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
            return f"username: {self.username} password: {self.password}"