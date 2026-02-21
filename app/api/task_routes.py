# app/api/task_routes.py — routes + exception handling + flash

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from app.service.task_service import TaskService
from app.exceptions import NotFoundError, ValidationError
from app.logger import logger

task_bp = Blueprint("tasks", __name__)

# Helper: check if user is logged in
def login_required():
    return "user_id" in session


# HTML Page: Task list with search & pagination
@task_bp.route("/", methods=["GET"])
def list_tasks_page():
    if not login_required():
        return redirect(url_for("auth.login"))

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    search = request.args.get("search")
    status = request.args.get("status")

    data = TaskService.list_tasks(page=page, per_page=per_page, search=search, status=status)
    return render_template("tasks.html", tasks=data["items"], pagination=data, request_args=request.args)


# API: Get all tasks (JSON)
@task_bp.route("/api", methods=["GET"])
def list_tasks_api():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    search = request.args.get("search")
    status = request.args.get("status")

    data = TaskService.list_tasks(page=page, per_page=per_page, search=search, status=status)
    return jsonify({
        "total": data["total"],
        "page": data["page"],
        "per_page": data["per_page"],
        "items": [t.to_dict() for t in data["items"]]
    })


# HTML Page: Add Task
@task_bp.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        data = request.form.to_dict()

        # 🔐 Inject logged-in user
        data["user_id"] = session.get("user_id")

        # 📁 Temporary: single default project
        data["project_id"] = 1

        TaskService.create_task(data)
        return redirect(url_for("tasks.list_tasks_page"))

    return render_template("add_task.html")


# HTML Page: Edit Task
@task_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    try:
        task = TaskService.get_task(task_id)
    except NotFoundError:
        flash("Task not found", "error")
        return redirect(url_for("tasks.list_tasks_page"))

    if request.method == "POST":
        try:
            TaskService.update_task(task_id, request.form.to_dict())
            flash("Task updated successfully.", "success")
            return redirect(url_for("tasks.list_tasks_page"))
        except ValidationError as e:
            flash(str(e), "error")
            return render_template("edit_task.html", task=task)

    return render_template("edit_task.html", task=task)


# HTML: Delete
@task_bp.route("/delete/<int:task_id>", methods=["GET"])
def delete_task(task_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    try:
        TaskService.delete_task(task_id)
        flash("Task deleted.", "success")
    except NotFoundError:
        flash("Task not found.", "error")

    return redirect(url_for("tasks.list_tasks_page"))


# API: single task view
@task_bp.route("/api/<int:task_id>", methods=["GET"])
def api_get_task(task_id):
    try:
        task = TaskService.get_task(task_id)
        return jsonify(task.to_dict())
    except NotFoundError:
        return jsonify({"error": "not found"}), 404
