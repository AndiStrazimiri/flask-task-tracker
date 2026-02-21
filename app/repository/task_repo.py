# app/repository/task_repo.py
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.extension import db
from app.models.task import Task
from app.logger import logger

class TaskRepository:

    @staticmethod
    def get_all(offset: int = 0, limit: int = 100, filters: dict = None, order_by=None) -> List[Task]:
        query = Task.query
        if filters:
            if 'status' in filters and filters['status']:
                query = query.filter(Task.status == filters['status'])
            if 'search' in filters and filters['search']:
                s = f"%{filters['search']}%"
                query = query.filter((Task.title.ilike(s)) | (Task.description.ilike(s)))

        if order_by is not None:
            query = query.order_by(order_by)

        logger.info("Repo: fetching tasks offset=%s limit=%s filters=%s", offset, limit, filters)
        return query.offset(offset).limit(limit).all()

    @staticmethod
    def count(filters: dict = None) -> int:
        query = Task.query
        if filters:
            if 'status' in filters and filters['status']:
                query = query.filter(Task.status == filters['status'])
            if 'search' in filters and filters['search']:
                s = f"%{filters['search']}%"
                query = query.filter((Task.title.ilike(s)) | (Task.description.ilike(s)))
        return query.count()

    @staticmethod
    def get_by_id(task_id: int) -> Optional[Task]:
        return Task.query.get(task_id)

    @staticmethod
    def create(task: Task) -> Task:
        try:
            db.session.add(task)
            db.session.commit()
            logger.info("Repo: created task id=%s", task.id)
            return task
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("Repo: create failed")
            raise

    @staticmethod
    def update() -> None:
        try:
            db.session.commit()
            logger.info("Repo: commit success on update")
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("Repo: update failed")
            raise

    @staticmethod
    def delete(task: Task) -> None:
        try:
            db.session.delete(task)
            db.session.commit()
            logger.info("Repo: deleted task id=%s", task.id)
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("Repo: delete failed")
            raise
