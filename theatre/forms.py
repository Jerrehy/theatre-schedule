from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, DateTimeField, SelectField, \
    IntegerField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired, NumberRange
from theatre.models import Employee


# Форма регистрации на сайте
class RegisterForm(FlaskForm):
    # Проверка наличия совпадений имён пользователей при создании нового пользователя
    def validate_username(self, username_to_check):
        user = Employee.get_employee_by_username(username_to_check.data)
        if user:
            raise ValidationError('Такое имя пользователя уже есть! Попробуйте придумать другое')

    def validate_fio(self, fio_to_check):
        fio = Employee.get_employee_by_fio(fio_to_check.data)
        if fio:
            raise ValidationError('У такого человека уже существует аккаунт! '
                                  'Если пароль и логин забыты, то обратитесь к администратору')

    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    username = StringField(label='Логин:', validators=[Length(min=6, max=20), DataRequired()])
    fio = TextAreaField(label='ФИО:', validators=[DataRequired()])
    birthday = DateField(label='Дата рождения:', validators=[DataRequired()])
    mobile_number = StringField(label='Мобильный телефон:')
    home_phone_number = StringField(label='Домашний телефон:')
    adress = TextAreaField(label='Адрес:', validators=[DataRequired()])
    password1 = PasswordField(label='Пароль:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Подтвердить пароль:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Создать аккаунт')


# Форма авторизации на сайте
class LoginForm(FlaskForm):
    username = StringField(label="Логин:", validators=[DataRequired()])
    password = PasswordField(label="Пароль:", validators=[DataRequired()])
    submit = SubmitField(label='Вход')


# Форма удаления пользователя
class DeleteForm(FlaskForm):
    submit = SubmitField(label="Удалить")


# Форма добавления спектакля
class AddPlay(FlaskForm):
    name_play = StringField('Название спектакля', validators=[Length(max=40), DataRequired()])
    stage_year = IntegerField('Год постановки', validators=[NumberRange(max=2022), DataRequired()])
    acts_number = IntegerField('Количество актов', validators=[NumberRange(max=10), DataRequired()])
    discription = TextAreaField('Описание спектакля', validators=[Length(max=50), DataRequired()])
    genre_name = SelectField('Название жанра', choices=[])
    author_fio = SelectField('ФИО автора', choices=[])
    author_birthday = SelectField('Год рождения автора', choices=[])
    submit_add_play = SubmitField(label='Добавить спектакль')


# Форма добавления сеанса в расписание
class AddSession(FlaskForm):
    name_session = SelectField('Название спектакля', choices=[])
    stage_year_session = SelectField('Год постановки', choices=[])
    type_session = SelectField('Тип', choices=['Спектакль', 'Репетиция'])
    date_time_session = DateTimeField('Дата и время', format='%Y-%m-%d %H:%M:%S')
    hall_number = SelectField('Номер зала', choices=[1, 2, 3, 4, 5, 6])
    submit_add_play = SubmitField(label='Добавить сеанс')


# Форма добавления новой позиции в расписании актёра
class AddRoleSchedule(FlaskForm):
    name_session = SelectField('Название спектакля', choices=[])
    stage_year_session = SelectField('Год постановки', choices=[])
    date_time_session = SelectField('Дата и время', choices=[])
    actor = SelectField('ФИО актёра', choices=[])
    role_in_play = StringField('Роль в спектакле', validators=[Length(max=40)])
    submit_add_role = SubmitField(label='Добавить позицию в расписание')


# Форма удаления спектакля из базы
class ChangePlay(FlaskForm):
    name_play = SelectField('Название спектакля', choices=[])
    stage_year = SelectField('Год постановки', choices=[])
    submit_del_play = SubmitField(label='Удалить спектакль')


# Форма удаления автора из базы
class DeleteAuthor(FlaskForm):
    author_fio = SelectField('ФИО автора', choices=[])
    author_birthday = SelectField('Год рождения автора', choices=[])
    submit_del_author = SubmitField(label='Удалить автора')


# Форма удаления жанра из базы
class DeleteGenre(FlaskForm):
    genre_name = SelectField('Название жанра', choices=[])
    submit_del_genre = SubmitField(label='Удалить жанр')


# Форма добавления нового автора
class AddAuthor(FlaskForm):
    author_fio = StringField('ФИО автора', validators=[Length(max=40), DataRequired()])
    author_birthday_year = IntegerField('Год рождения автора', validators=[NumberRange(max=2022), DataRequired()])
    submit_add_author = SubmitField(label='Добавить автора')


# Форма добавления нового жанра
class AddGenre(FlaskForm):
    genre_name = StringField('Название жанра', validators=[Length(max=30), DataRequired()])
    submit_add_genre = SubmitField(label='Добавить жанр')


# Форма изменения должности сотрудника, а также удаление его из базы
class ChangeEmployee(FlaskForm):
    employee_fio = SelectField('ФИО сотрудника', choices=[])
    position_name = SelectField('Название должности', choices=[])
    submit_del_mpl = SubmitField(label="Удалить аккаунт")
    submit_up_empl = SubmitField(label='Изменить должность')


# Форма удаления сеанса из базы
class ChangeSession(FlaskForm):
    session_name = SelectField('Название спектакля', choices=[])
    stage_year = SelectField('Год постановки', choices=[])
    date_time_session = SelectField('Время сеанса', choices=[])
    hall_number = SelectField('Номер зала', choices=[])
    submit_del_ses = SubmitField(label="Удалить сеанс")


# Форма удаления позиции из расписания актёров
class RoleEmployee(FlaskForm):
    session_name = SelectField('Название спектакля', choices=[])
    stage_year = SelectField('Год постановки', choices=[])
    date_time_session = SelectField('Время сеанса', choices=[])
    employee_fio = SelectField('ФИО сотрудника', choices=[])
    submit_del_role = SubmitField(label="Удалить позицию в расписании")


# Форма редактирования профиля пользователя
class EmployeeUpdate(FlaskForm):
    employee_fio = TextAreaField(label='Новое ФИО', validators=[DataRequired()])
    birthday = DateField(label='Новая дата рождения', validators=[DataRequired()])
    mobile_phone_number = StringField(label='Новый мобильный телефон')
    home_phone_number = StringField(label='Новый домашний телефон')
    address = TextAreaField(label='Новый адрес', validators=[DataRequired()])
    submit_employee_update = SubmitField(label="Подтвердить изменения", validators=[DataRequired()])
