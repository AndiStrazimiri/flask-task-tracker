# app/config.py
import os

class Config:
    # update the password and DB name if needed
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:Informatike10Biznesi!@localhost:3306/tasktracker"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
