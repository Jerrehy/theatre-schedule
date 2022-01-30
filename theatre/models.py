from flask import flash, redirect, url_for
from flask_login import UserMixin
from theatre import login_manager
from theatre import db


# Функция обработки ошибки при неправильном удалении из базы
def DbErrorDel():
    flash('Проверьте зависимости перед удалением', category='danger')
    db.session.rollback()


# Функция обработки ошибки при неправильном изменении в базе
def DbErrorAdd():
    flash('Проверьте правильность введённых данных', category='danger')
    db.session.rollback()


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


# Подключение таблиц из базы данных

# Таблица с данными о репертуаре спектаклей
class PlayInfo(db.Model):
    __tablename__ = 'play_info'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех информации о спектаклях
    @staticmethod
    def get_all_play_info():
        return PlayInfo.query.order_by(PlayInfo.name_play).all()

    # Метод получения всей информации по названию спектакля
    @staticmethod
    def get_all_play_info_by_name_play(name_play):
        return PlayInfo.query.filter_by(name_play=name_play).all()

    # Метод добавления нового спектакля
    @staticmethod
    def add_play_info(name_play, stage_year, acts_number, discription, genre_name, author_fio, author_birthday_year):
        play_to_create = PlayInfo(name_play=name_play, stage_year=stage_year, acts_number=acts_number,
                                  discription=discription, genre_name=genre_name, author_fio=author_fio,
                                  author_birthday_year=author_birthday_year)

        try:
            db.session.add(play_to_create)
            db.session.commit()
        except:
            DbErrorAdd()

    # Метод удаления спектакля
    @staticmethod
    def delete_play_info_by_name_and_stage_year(name_play, stage_year):
        try:
            PlayInfo.query.filter_by(name_play=name_play, stage_year=stage_year).delete()
            db.session.commit()
        except:
            DbErrorAdd()


# Подключение таблицы жанров
class Genre(db.Model):
    __tablename__ = 'genre'
    __table_args__ = {'extend_existing': True}

    # Метод получения списка всех жанров
    @staticmethod
    def get_genre():
        return Genre.query.order_by(Genre.genre_name).all()

    # Метод добавления нового жанра
    @staticmethod
    def add_genre(genre_name):
        new_genre = Genre(genre_name=genre_name)

        try:
            db.session.add(new_genre)
            db.session.commit()
        except:
            DbErrorAdd()

    # Метод удаления жанра из списка
    @staticmethod
    def delete_genre(genre_name):
        try:
            Genre.query.filter_by(genre_name=genre_name).delete()
            db.session.commit()
        except:
            DbErrorDel()


# Подключение таблицы авторов
class Author(db.Model):
    __tablename__ = 'author'
    __table_args__ = {'extend_existing': True}

    # Метод получения всей информации об авторах
    @staticmethod
    def get_author():
        return Author.query.order_by(Author.author_fio).all()

    # Метод получения всех дат по авторам
    @staticmethod
    def get_all_author_birthday_year_by_fio(author_fio):
        return Author.query.filter_by(author_fio=author_fio).all()

    # Метод удаления автора
    @staticmethod
    def delete_author(author_fio):
        try:
            Author.query.filter_by(author_fio=author_fio).delete()
            db.session.commit()
        except:
            DbErrorDel()

    # Метод добавления нового автора
    @staticmethod
    def add_author(author_fio, author_birthday_year):
        new_author = Author(author_fio=author_fio, author_birthday_year=author_birthday_year)
        try:
            db.session.add(new_author)
            db.session.commit()
        except:
            DbErrorAdd()


# Подключение таблицы сотрудников
class Employee(db.Model, UserMixin):
    __tablename__ = 'employee'
    __table_args__ = {'extend_existing': True}

    # Создание связи по внешней ссылке
    employee_position = db.relationship('EmployeePosition', backref='employee_position', uselist=False)

    personal_number = db.Column(db.Integer(), primary_key=True)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.personal_number

    # Метод получения всей информации о сотрудниках
    @staticmethod
    def get_employee():
        return Employee.query.order_by(Employee.fio).all()

    # Метод получения информации о сотруднике по его персональному номеру
    @staticmethod
    def get_employee_by_id(id_user):
        return Employee.query.filter_by(personal_number=id_user).first()

    # Методу получения информации о сотруднике по его логину в системе
    @staticmethod
    def get_employee_by_username(username):
        return Employee.query.filter_by(username=username).first()

    # Метод получения информации о сотруднике по его фамилии
    @staticmethod
    def get_employee_by_fio(fio):
        return Employee.query.filter_by(fio=fio).first()

    # Метод удаления аккаунта сотрудника
    @staticmethod
    def delete_employee_by_fio(fio):
        try:
            Employee.query.filter_by(fio=fio).delete()
            db.session.commit()
        except:
            DbErrorDel()

    # Метод изменения информации о сотруднике
    @staticmethod
    def update_info_employee(employee_id, fio, birthday, mobile_phone, home_phone, address):
        try:
            employee_for_update = Employee.get_employee_by_id(employee_id)
            employee_for_update.fio = fio
            employee_for_update.birthday = birthday
            employee_for_update.mobile_number = mobile_phone
            employee_for_update.home_phone_number = home_phone
            employee_for_update.adress = address
            db.session.commit()
        except:
            DbErrorAdd()

    # Метод добавления нового сотрудника
    @staticmethod
    def add_employee(username, fio, birthday, mobile_number, home_phone_number, adress, password):
        # Заполнение введённых данных о пользователе
        user_to_create = Employee(username=username, fio=fio, birthday=birthday, mobile_number=mobile_number,
                                  home_phone_number=home_phone_number, adress=adress, password=password)

        # Механизм добавления нового пользователя в базу
        try:
            db.session.add(user_to_create)
            db.session.commit()
        except:
            DbErrorAdd()
            return redirect(url_for('auth.register_page'))


# Подключение таблицы со списком ролей
class Position(db.Model):
    __tablename__ = 'position'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех должностей
    @staticmethod
    def get_position():
        return Position.query.all()

    # Метод получения ID должности по её именованию
    @staticmethod
    def get_position_id_by_name(position_name):
        position = Position.query.filter_by(position_name=position_name).one()
        return position.id_position


# Подключение таблицы со связью позиции сотрудника и его аккаунта
class EmployeePosition(db.Model):
    __tablename__ = 'employee_position'
    __table_args__ = {'extend_existing': True}

    # Создание связи по внешней ссылке
    position = db.relationship('Position', backref='position', uselist=False)

    # Метод получения всех позиций
    @staticmethod
    def get_all_employee_position():
        return EmployeePosition.query.all()

    # Метод получения позиции сотрудника по его персональному номеру
    @staticmethod
    def get_employee_position_for_personal_number(personal_number):
        return EmployeePosition.query.filter_by(personal_number=personal_number).all()

    # Метод добавления информации о новом сотруднике
    @staticmethod
    def add_employee_position(personal_number, id_position):
        try:
            employee_position_for_add = EmployeePosition(personal_number=personal_number, id_position=id_position)
            db.session.add(employee_position_for_add)
            db.session.commit()
        except:
            DbErrorAdd()

    # Обновление должности назначенного сотрудника
    @staticmethod
    def update_employee_position(personal_number, id_position):
        try:
            employee_for_update = EmployeePosition.get_employee_position_for_personal_number(personal_number)
            employee_for_update.id_position = id_position
            db.session.commit()
        except:
            DbErrorAdd()


# Подключение таблицы с общим расписанием сеансов
class Schedule(db.Model):
    __tablename__ = 'schedule'
    __table_args__ = {'extend_existing': True}

    # Метод получения всей информации по расписанию
    @staticmethod
    def get_schedule():
        return Schedule.query.all()

    # Метод удаления сеанса из расписания
    @staticmethod
    def delete_schedule(name_play, date_and_time, hall_number):
        try:
            Schedule.query.filter_by(name_play=name_play, date_and_time=date_and_time, hall_number=hall_number).delete()
            db.session.commit()
        except:
            DbErrorDel()

    # Метод получения информации о расписании по названию спектакля, году постановки и времени проведения сеанса
    @staticmethod
    def get_schedule_by_name_play_stage_year_datetime(name_play, stage_year, date_and_time):
        return Schedule.query.filter_by(name_play=name_play, stage_year=stage_year, date_and_time=date_and_time).one()

    # Метод получения информации о расписании по названию спектакля
    @staticmethod
    def get_all_schedule_by_name_play(name_play):
        return Schedule.query.filter_by(name_play=name_play).all()

    # Метод добавления нового сеанса в расписание
    @staticmethod
    def add_schedule_position(date_and_time, hall_number, type_play, name_play, stage_year):
        new_schedule = Schedule(date_and_time=date_and_time, hall_number=hall_number, type_play=type_play,
                                name_play=name_play, stage_year=stage_year)
        try:
            db.session.add(new_schedule)
            db.session.commit()
        except:
            DbErrorAdd()


# Подключение таблицы с расписанием сотрудников
class ActorRole(db.Model):
    __tablename__ = 'actor_role'
    __table_args__ = {'extend_existing': True}

    employee = db.relationship('Employee', backref='employee', uselist=False)

    # Метод получения всего расписания сотрудников
    @staticmethod
    def get_actor_role():
        return ActorRole.query.all()

    # Метод выделения определённых позиций в расписании по названию спектакля
    @staticmethod
    def get_actor_role_by_name_play(name_play):
        return ActorRole.query.filter_by(name_play=name_play).all()

    # Методе выделения определённых позиций в расписании по персональному номеру сотрудника
    @staticmethod
    def get_actor_role_by_id(id_user):
        return ActorRole.query.filter_by(personal_number_employee=id_user).all()

    # Метод добавления новой позиции в расписание сотрудников
    @staticmethod
    def add_actor_role(personal_number_employee, hall_number, date_and_time, name_role, name_play, stage_year):
        role_for_schedule = ActorRole(personal_number_employee=personal_number_employee, hall_number=hall_number,
                                      date_and_time=date_and_time, name_role=name_role, name_play=name_play,
                                      stage_year=stage_year)
        try:
            db.session.add(role_for_schedule)
            db.session.commit()
        except:
            DbErrorAdd()

    # Метод удаления позиции из расписания актёров
    @staticmethod
    def delete_actor_role_position(name_play, date_and_time, personal_number_employee):
        try:
            ActorRole.query.filter_by(name_play=name_play, date_and_time=date_and_time,
                                      personal_number_employee=personal_number_employee).delete()
            db.session.commit()
        except:
            DbErrorDel()
            return redirect(url_for('route_schedule_employee.schedule_employee'))
