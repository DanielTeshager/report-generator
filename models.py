import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

database_name = "Report_Generator"
# connect to sqllite db

database_path = 'sqlite:////{}'.format(os.path.join(os.path.dirname(__file__), database_name))

db = SQLAlchemy()

"""
    setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Sentence

"""


class Sentence(db.Model):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    def __init__(self, title, category):
        self.title = title
        self.category = category

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category
        }


