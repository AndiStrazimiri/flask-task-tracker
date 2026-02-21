# app/service/task_service.py --- service with validation + pagination
from typing import Dict, Any
from app.repository.task_repo import TaskRepository
from app.models.task import Task
from app.exceptions import NotFoundError, ValidationError
from app.logger import logger

class TaskService:

    @staticmethod
    def list_tasks(page: int = 1, per_page: int = 10, search: str = None, status: str = None) -> Dict[str, Any]:
        page = max(1, int(page))
        per_page = max(1, min(100, int(per_page)))
        offset = (page - 1) * per_page
        filters = {}
        if search:
            filters['search'] = search.strip()
        if status:
            filters['status'] = status.strip()

        total = TaskRepository.count(filters)
        items = TaskRepository.get_all(offset=offset, limit=per_page, filters=filters, order_by=Task.created_at.desc())
        logger.info("Service: list tasks page=%s per_page=%s total=%s", page, per_page, total)
        return {"total": total, "page": page, "per_page": per_page, "items": items}

    @staticmethod
    def get_task(task_id: int) -> Task:
        task = TaskRepository.get_by_id(task_id)
        if not task:
            logger.warning("Service: task not found id=%s", task_id)
            raise NotFoundError(f"Task with id {task_id} not found")
        return task

    @staticmethod
    def create_task(data: dict):
        title = data.get("title")
        user_id = data.get("user_id")
        project_id = data.get("project_id")

        if not title:
            raise ValidationError("Task title is required")

        if not user_id:
            raise ValidationError("User must be logged in")

        if not project_id:
            raise ValidationError("Project is required")

        task = Task(
            title=title,
            description=data.get("description"),
            status=data.get("status", "Pending"),
            user_id=user_id,
            project_id=project_id
        )

        return TaskRepository.create(task)


    @staticmethod
    def update_task(task_id: int, data: Dict[str, Any]) -> Task:
        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        if "title" in data:
            title = (data.get("title") or "").strip()
            if not title:
                raise ValidationError("Title cannot be empty")
            task.title = title
        if "description" in data:
            task.description = data.get("description")
        if "status" in data:
            task.status = data.get("status")
        TaskRepository.update()
        logger.info("Service: task updated id=%s", task.id)
        return task

    @staticmethod
    def delete_task(task_id: int) -> bool:
        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        TaskRepository.delete(task)
        logger.info("Service: task deleted id=%s", task_id)
        return True
    
    