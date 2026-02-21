from app.repository.user_repo import UserRepository
from app.exceptions import ValidationError

class UserService:

    @staticmethod
    def register_user(data: dict):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise ValidationError("Username and password are required")

        existing = UserRepository.get_by_username(username)
        if existing:
            raise ValidationError("Username already exists")

        return UserRepository.create(username=username, password=password)

    @staticmethod
    def authenticate(username, password):
        if not username or not password:
            return None

        user = UserRepository.get_by_username(username)
        if user and user.password == password:
            return user

        return None
