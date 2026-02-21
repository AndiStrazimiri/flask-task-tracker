# app/service/project_service.py
from typing import List
from app.repository.project_repo import ProjectRepository
from app.repository.user_repo import UserRepository
from app.exceptions import NotFoundError, ValidationError
from app.models.project import Project
from app.logger import logger

class ProjectService:
    """Business logic for Projects."""

    @staticmethod
    def create_project(title: str, user_id: int) -> Project:
        title = (title or "").strip()
        if not title:
            logger.warning("ProjectService.create_project: empty title")
            raise ValidationError("Project title is required")

        # ensure user exists
        user = UserRepository.get_by_id(user_id)
        if not user:
            logger.warning("ProjectService.create_project: user not found id=%s", user_id)
            raise NotFoundError("User not found")

        project = ProjectRepository.create(title=title, user_id=user_id)
        logger.info("ProjectService.create_project: project id=%s created", project.id)
        return project

    @staticmethod
    def get_user_projects(user_id: int) -> List[Project]:
        # optionally validate user exists
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return ProjectRepository.get_by_user(user_id)

    @staticmethod
    def get_project(project_id: int) -> Project:
        proj = ProjectRepository.get_by_id(project_id)
        if not proj:
            raise NotFoundError("Project not found")
        return proj

    @staticmethod
    def delete_project(project_id: int) -> None:
        proj = ProjectRepository.get_by_id(project_id)
        if not proj:
            raise NotFoundError("Project not found")
        ProjectRepository.delete(proj)
