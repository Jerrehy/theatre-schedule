from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Экземлпяр приложения
app = Flask(__name__)

# Данные конфигурации подключения к БД
dialect = 'postgresql'
username = 'postgres'
password = 'Qwerty7'
host = 'localhost'
db_name = 'theater_schedule'

# Настройки для экземляра: секретный ключ запуска и путь к БД
app.config['SQLALCHEMY_DATABASE_URI'] = f'{dialect}://{username}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '75343b374aa2aaa269e856ad'


# Подключение БД к приложению
db = SQLAlchemy(app)

# Настройка пользовательского входа
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подлючение файла с маршрутами
from theatre import routes
