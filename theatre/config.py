
class Config:
    # Данные конфигурации подключения к БД
    dialect = 'postgresql'
    username = 'postgres'
    password = 'Qwerty7'
    host = 'localhost'
    db_name = 'theater_schedule'

    # Настройки для экземляра: секретный ключ запуска и путь к БД
    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '75343b374aa2aaa269e856ad'
