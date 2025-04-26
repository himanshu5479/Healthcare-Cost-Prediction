from extensions import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, email, username, password, is_hashed=False):
        self.email = email
        self.username = username
        self.password = password if is_hashed else generate_password_hash(password)

    def save(self):
        mongo.db.users.insert_one({
            "email": self.email,
            "username": self.username,
            "password": self.password
        })

    @staticmethod
    def find_by_email(email):
        user_data = mongo.db.users.find_one({"email": email})
        if user_data:
            return User(
                email=user_data["email"],
                username=user_data["username"],
                password=user_data["password"],
                is_hashed=True
            )
        return None

    def check_password(self, password):
        return check_password_hash(self.password, password)
