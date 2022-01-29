from flask import Flask
from flask_login import LoginManager
from theatre.config import Config
from flask_sqlalchemy import SQLAlchemy

# Создание объекта приложения
app = Flask(__name__)
# Ввод конфиг файла для приложения
app.config.from_object(Config)

# Подключение готовой базы данных
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# Настройка пользовательского входа с помощь логин менеджера
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подключение узлов с методами к приложению
from theatre.user.user import user
from theatre.auth.auth import auth
from theatre.admin.admin import admin
from theatre.moder.route_schedule_session import route_schedule_session
from theatre.moder.route_play_atr import route_play_atr
from theatre.moder.route_play_info import route_play_info
from theatre.moder.route_schedule_employee import route_schedule_employee
from theatre.employee_schedule.employee_schedule import employee_schedule

app.register_blueprint(user)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(route_schedule_session)
app.register_blueprint(route_play_atr)
app.register_blueprint(route_play_info)
app.register_blueprint(route_schedule_employee)
app.register_blueprint(employee_schedule)
