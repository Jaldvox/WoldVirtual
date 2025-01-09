class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}')"

class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user_id):
        self.users = [user for user in self.users if user.user_id != user_id]

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def list_users(self):
        return self.users