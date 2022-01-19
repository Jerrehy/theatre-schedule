from flask_login import UserMixin
from sqlalchemy.ext.automap import automap_base
from theatre import db, login_manager


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Employee).get(int(user_id))


# Метод подключающий рефлексию для транспортировки базы в приложение
Base = automap_base()


# Подключение таблиц из базы данных
class PlayInfo(Base):
    __tablename__ = 'play_info'


class Genre(Base):
    __tablename__ = 'genre'


class Author(Base):
    __tablename__ = 'author'


class Employee(Base, UserMixin):
    __tablename__ = 'employee'

    personal_number = db.Column(db.Integer(), primary_key=True)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.personal_number


class Position(Base):
    __tablename__ = 'position'


class Schedule(Base):
    __tablename__ = 'schedule'


class ActorRole(Base):
    __tablename__ = 'actor_role'