import bcrypt
from models import utility


def get_user_if_valid(email, plain_text_password):
    results = utility.sql_read(f"SELECT * FROM users WHERE email=%s;", [email])
    if len(results):
        user = results[0]
        user_formatted = {
            "id": user[0],
            "email": user[1],
            "username": user[2],
            "password_hash": user[3],
        }
        # return user only if password matches
        if bcrypt.checkpw(
            plain_text_password.encode(), user_formatted["password_hash"].encode()
        ):
            return user_formatted
        return None
    return None


def add_user(email, username, plain_text_password):
    password_hash = bcrypt.hashpw(
        plain_text_password.encode(), bcrypt.gensalt()
    ).decode()
    utility.sql_write(
        "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s);",
        [email, username, password_hash],
    )
