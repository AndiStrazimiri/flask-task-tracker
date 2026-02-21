# app/repository/project_repo.py
from typing import List, Optional
from app.extension import db
from app.models.project import Project
from app.logger import logger
from sqlalchemy.exc import SQLAlchemyError

class ProjectRepository:
    """Repository for Project DB operations."""

    @staticmethod
    def create(title: str, user_id: int) -> Project:
        project = Project(title=title, user_id=user_id)
        try:
            db.session.add(project)
            db.session.commit()
            logger.info("ProjectRepository.create: created project id=%s", project.id)
            return project
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("ProjectRepository.create: DB error")
            raise

    @staticmethod
    def get_by_id(project_id: int) -> Optional[Project]:
        return Project.query.get(project_id)

    @staticmethod
    def get_by_user(user_id: int) -> List[Project]:
        return Project.query.filter_by(user_id=user_id).all()

    @staticmethod
    def delete(project: Project) -> None:
        try:
            db.session.delete(project)
            db.session.commit()
            logger.info("ProjectRepository.delete: deleted project id=%s", project.id)
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("ProjectRepository.delete: DB error")
            raise

    @staticmethod
    def update() -> None:
        try:
            db.session.commit()
            logger.info("ProjectRepository.update: commit success")
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("ProjectRepository.update: DB error")
            raise
