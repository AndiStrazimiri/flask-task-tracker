# app/models/project.py
from app.extension import db

class Project(db.Model):
    """
    Project model:
    - id
    - title
    - user_id (FK -> users.id)
    - relationship to tasks
    """
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationship: one project has many tasks
    tasks = db.relationship("Task", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project id={self.id} title={self.title}>"
