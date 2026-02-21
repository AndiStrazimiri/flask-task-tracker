from typing import Optional
from app.extension import db
from app.models.user import User
from app.logger import logger
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:

    @staticmethod
    def create(username: str, password: str) -> User:
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            logger.info("UserRepository.create: created user id=%s", user.id)
            return user
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("UserRepository.create: DB error")
            raise

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

