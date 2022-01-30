from flask import Blueprint, render_template, redirect, url_for, flash, session
from theatre.models import Employee
from theatre.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user

# Создание узла для обращению к функциям регистрация, авторизации и выхода из аккаунта
auth = Blueprint('auth', __name__, template_folder="templates")


# Маршрут с логикой организации регистрации на сайте через форму с ошибками и добавлением в БД
@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    # Проверка нажатия кнопки "Создать аккаунт"
    if form.validate_on_submit():
        Employee.add_employee(username=form.username.data, fio=form.fio.data, birthday=form.birthday.data,
                              mobile_number=form.mobile_number.data, home_phone_number=form.home_phone_number.data,
                              adress=form.adress.data, password=form.password1.data)
        return redirect(url_for('auth.login_page'))

    # Механизм вывода ошибок при создании нового пользователя
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка при создании нового пользователя: {err_msg}', category='danger')

    # Вовзрашение html шаблона с формой регистрации
    return render_template('register.html', form=form)


# Маршрут с логикой авторизации на сайте с обращением к таблице пользователей в БД
# При успешном входе в переменной session сохраняется идентификатор должности пользователя
@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # Проверка нажатия на клавишу "Вход"
    if form.validate_on_submit():
        attempted_user = Employee.get_employee_by_username(username=form.username.data)
        # Проверка на наличие пользователя в базе
        if attempted_user:
            # Проверка на совпадение введённого пароля и пароля в базе
            if form.password.data in attempted_user.password:
                login_user(attempted_user)
                flash(f'Вход выполнен успешно! Вы зашли как {attempted_user.username}', category='success')
                if attempted_user.employee_position:
                    session['role'] = attempted_user.employee_position.id_position
                else:
                    session['role'] = None
            else:
                flash('Пароль неверный! Попробуйте снова', category='danger')

            return redirect(url_for('user.home_page'))
        else:
            flash('Логин не найден! Попробуйте снова', category='danger')

    return render_template('login.html', form=form)


# Маршрут с логикой выхода из аккаунта на сайте - организован через flask_login, который выходит из сессии
# Обнуление переменной session['role'] и возвращение на главную страницу
@auth.route('/logout')
def logout_page():
    # Выход пользователя из аккаунта
    logout_user()
    # Очистка текущей роли пользователя
    session.pop('role', None)
    # Очистка куки с дополнительными данными о пользователе
    session.clear()

    flash("Вы вышли из аккаунта", category='info')
    return redirect(url_for('user.home_page'))
