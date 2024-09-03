from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .userModel import User
from .questionModel import Question