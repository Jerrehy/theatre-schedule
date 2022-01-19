from theatre import app
from flask import render_template, redirect, url_for, flash, session, request
from theatre.models import Genre, Author, PlayInfo, Employee, Position, Schedule, ActorRole, Base
from theatre.forms import RegisterForm, LoginForm, ChangePlay, AddPlay, DeleteAuthor, DeleteGenre, \
    AddAuthor, AddGenre, ChangeEmployee, ChangeSession, RoleEmployee, AddRoleSchedule, AddSession
from theatre import db
from flask_login import login_user, logout_user, login_required, current_user


# Запрет Automap создавать отношения самостоятельно
def generate_relationships(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    return None


# Механизм копирования данных из базы
Base.prepare(generate_relationship=generate_relationships)


# Функция обработки ошибки при неправильном удалении из базы
def DbErrorDel():
    flash('Проверьте зависимости перед удалением', category='danger')
    db.session.rollback()


# Функция обработки ошибки при неправильном изменении в базе
def DbErrorAdd():
    flash('Проверьте правильность введённых данных', category='danger')
    db.session.rollback()


# Начальная страница сайта
@app.route('/')
@app.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html')


# Страница профиля пользователя
# Ко всем последующим страницам подключен механизм проверки авторизации
# Декоратор @login_required
@app.route('/')
@app.route('/profile', methods=['GET'])
@login_required
def profile_page():
    employer = db.session.query(Employee).filter_by(personal_number=current_user.get_id()).first()
    return render_template('profile.html', employee=employer)


# Страница информации о спектаклях в театре, которые могут быть поставлены
# Работает при наличии определённо роли у пользователя - Модератор
# Роль с идентификатором 7
@app.route('/play-info', methods=['GET', 'POST'])
@login_required
def play_info():
    if session['role'] == 7:
        # Подключение форм для изменения таблицы со спектаклями
        change_play_form = ChangePlay()
        add_play_form = AddPlay()

        # Заполнение форм заранее прописанными в базе данными
        # Оформление выпадающих списков

        # Обращение к базе данных - таблица "Спектакль"
        available_plays = db.session.query(PlayInfo).all()

        # Выпадающий список доступных произведений
        change_play_form.name_play.choices = list(set([i.name_play for i in available_plays]))

        # Обращение к базе данных - к таблицам "Автор" и "Жанр"
        available_authors = db.session.query(Author).all()
        available_genres = db.session.query(Genre).all()

        # Выпадающий список доступных авторов
        add_play_form.author_fio.choices = list(set([i.author_fio for i in available_authors]))

        # Выпадающий список доступных жанров
        add_play_form.genre_name.choices = [i.genre_name for i in available_genres]

        # Метод удаления спектаклей в театре
        if change_play_form.validate_on_submit():
            try:
                db.session.query(PlayInfo).filter_by(name_play=change_play_form.name_play.data).delete()
                db.session.commit()
            except:
                DbErrorAdd()

            return redirect(url_for('play_info'))

        # Метод добавления нового спектакля
        elif add_play_form.validate_on_submit():
            author_birthday_year = db.session.query(Author).filter_by(author_fio=
                                                                      add_play_form.author_fio.data).first()

            play_to_create = PlayInfo(name_play=add_play_form.name_play.data, stage_year=add_play_form.stage_year.data,
                                      acts_number=add_play_form.acts_number.data,
                                      discription=add_play_form.discription.data,
                                      genre_name=add_play_form.genre_name.data,
                                      author_fio=add_play_form.author_fio.data,
                                      author_birthday_year=author_birthday_year.author_birthday_year)

            try:
                db.session.add(play_to_create)
                db.session.commit()
            except:
                DbErrorAdd()

            return redirect(url_for('play_info'))

        return render_template('play-info.html', plays=available_plays, change_play_form=change_play_form,
                               add_play_form=add_play_form)
    else:
        return render_template('home.html')


# Страница с информацией о используемых авторах и жанрах
@app.route('/play-atr', methods=['GET', 'POST'])
@login_required
def play_atr():
    if session['role'] == 7:
        # Подключение форм для удаления автора и удаления жанра
        delete_author_form = DeleteAuthor()
        delete_genre_form = DeleteGenre()

        # Подключение форм для добавления нового автора и нового жанра
        add_genre_form = AddGenre()
        add_author_form = AddAuthor()

        # Подбор из таблицы авторов всех созданных ранее записей и вывод в выпадающий список
        available_authors = db.session.query(Author).all()
        delete_author_form.author_fio.choices = [i.author_fio for i in available_authors]

        # Подбор из таблицы жанроов всех созданных ранее записей и вывод в выпадающий список
        available_genres = db.session.query(Genre).all()
        delete_genre_form.genre_name.choices = [i.genre_name for i in available_genres]

        # Метод удаления автора
        if delete_author_form.validate_on_submit():
            try:
                db.session.query(Author).filter_by(author_fio=delete_author_form.author_fio.data).delete()
                db.session.commit()
            except:
                DbErrorDel()

            return redirect(url_for('play_atr'))

        # Метод удаления жанра
        elif delete_genre_form.validate_on_submit():
            try:
                db.session.query(Genre).filter_by(genre_name=delete_genre_form.genre_name.data).delete()
                db.session.commit()
            except:
                DbErrorDel()

            return redirect(url_for('play_atr'))

        # Метод добавления нового автора
        elif add_author_form.validate_on_submit():
            new_author = Author(author_fio=add_author_form.author_fio.data,
                                author_birthday_year=add_author_form.author_birthday_year.data)
            try:
                db.session.add(new_author)
                db.session.commit()
            except:
                DbErrorAdd()

            return redirect(url_for('play_atr'))

        # Метод добавления нового жанра
        elif add_genre_form.validate_on_submit():
            new_genre = Genre(genre_name=add_genre_form.genre_name.data)

            try:
                db.session.add(new_genre)
                db.session.commit()
            except:
                DbErrorAdd()

            return redirect(url_for('play_atr'))

        return render_template('play-atr.html', authors=available_authors, genres=available_genres,
                               delete_author_form=delete_author_form, delete_genre_form=delete_genre_form,
                               add_genre_form=add_genre_form, add_author_form=add_author_form)
    else:
        return render_template('home.html')


# Страница с информацией о сотрудниках и их должностях
@app.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():
    if session['role'] == 8:
        # Подключение формы для изменения информации о сотруднике или для удаления его из базы
        change_form = ChangeEmployee()

        # Извлечение информации о сотрудниках и доступных должностях из базы
        available_employee = db.session.query(Employee).order_by(Employee.personal_number).all()
        available_position = db.session.query(Position).order_by(Position.id_position).all()

        # Создание выпадающих списков для вывода доступных сотрудников и доступных позиций
        change_form.position_name.choices = [i.position_name for i in available_position]
        change_form.employee_fio.choices = [i.fio for i in available_employee]

        # Метод изменения/удаления сотрудника
        if change_form.validate_on_submit():
            # Удаление сотрудника
            if change_form.submit_del_mpl.data:
                try:
                    db.session.query(Employee).filter_by(fio=change_form.employee_fio.data).delete()
                    db.session.commit()
                except:
                    DbErrorDel()

                return redirect(url_for('employee'))

            # Изменение должности сотрудника
            elif change_form.submit_up_empl.data:
                try:
                    employee_for_update = db.session.query(Employee).filter_by(fio=change_form.employee_fio.data).one()
                    new_position = db.session.query(Position).filter_by(
                        position_name=change_form.position_name.data).one()
                    employee_for_update.id_position = new_position.id_position
                    db.session.commit()
                except:
                    DbErrorAdd()

                return redirect(url_for('employee'))

        return render_template('employee.html', employers=available_employee, positions=available_position,
                               change_form=change_form)

    else:
        return render_template('home.html')


@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if session['role'] == 7:
        # Подключение таблиц с расписанием сеансов и расписанием актёров
        tabletop = db.session.query(Schedule).all()
        roles = db.session.query(ActorRole).all()

        # Обращение к таблицам PlayInfo и Employee
        # Для корректного ввода информации из них
        plays = db.session.query(PlayInfo).all()
        employers = db.session.query(Employee).all()

        # Добавление форм для добавления сеанса и позиции в расписании актёров
        add_session_form = AddSession()
        add_schedule_role_form = AddRoleSchedule()

        # Добавление форм для удаления сеанса и позиции в расписании актёров
        session_form = ChangeSession()
        role_form = RoleEmployee()

        # Выпадающие списки для удаления и редактирования расписания сеансов
        session_form.session_name.choices = list(set([i.name_play for i in tabletop]))
        session_form.date_time_session.choices = list(set([i.date_and_time for i in tabletop]))
        session_form.hall_number.choices = list(set([i.hall_number for i in tabletop]))

        # Выпадающие списки для удаления и редактирования расписания актёров
        role_form.session_name.choices = list(set([i.name_play for i in roles]))
        role_form.employee_fio.choices = list(set([i.employee.fio for i in roles]))
        role_form.date_time_session.choices = list(set([i.date_and_time for i in roles]))

        # Выпадающий список доступных постановок
        add_session_form.name_session.choices = list(set([i.name_play for i in plays]))

        # Выпадающие списки для добавления новых позиций в расписании
        add_schedule_role_form.name_session.choices = list(set([i.name_play for i in tabletop]))
        add_schedule_role_form.actor.choices = list(set([i.fio for i in employers if i.id_position
                                                         and i.id_position != 7 and i.id_position != 8]))
        add_schedule_role_form.date_time_session.choices = list(set([i.date_and_time for i in tabletop]))

        # Метод удаления сеанса спектакля из расписания
        if session_form.validate_on_submit():
            try:
                db.session.query(Schedule).filter_by(name_play=session_form.session_name.data,
                                                     date_and_time=session_form.date_time_session.data,
                                                     hall_number=session_form.hall_number.data).delete()
                db.session.commit()
            except:
                DbErrorDel()

            return redirect(url_for('schedule'))

        # Метод удаления позиции из расписания сотрудников
        elif role_form.validate_on_submit():
            my_employee = db.session.query(Employee).filter_by(fio=role_form.employee_fio.data).first()

            try:
                db.session.query(ActorRole).filter_by(name_play=role_form.session_name.data,
                                                      date_and_time=role_form.date_time_session.data,
                                                      personal_number_employee=my_employee.personal_number).delete()
                db.session.commit()

            except:
                DbErrorDel()

            return redirect(url_for('schedule'))

        # Метод добавления нового сеанса спектакля в расписание театра
        elif add_session_form.validate_on_submit():
            play_for_add = db.session.query(PlayInfo).filter_by(name_play=add_session_form.name_session.data).first()

            new_schedule = Schedule(date_and_time=add_session_form.date_time_session.data,
                                    hall_number=add_session_form.hall_number.data,
                                    type_play=add_session_form.type_session.data,
                                    name_play=play_for_add.name_play,
                                    stage_year=play_for_add.stage_year)

            try:
                db.session.add(new_schedule)
                db.session.commit()
            except:
                DbErrorAdd()

            return redirect(url_for('schedule'))

        # Метод добавления новой позиции в расписании сотрудников
        elif add_schedule_role_form.validate_on_submit():
            play_for_info = db.session.query(Schedule).filter_by(name_play=
                                                                 add_schedule_role_form.name_session.data).first()
            actor_for_info = db.session.query(Employee).filter_by(fio=add_schedule_role_form.actor.data).first()

            role_for_schedule = ActorRole(personal_number_employee=actor_for_info.personal_number,
                                          hall_number=play_for_info.hall_number,
                                          date_and_time=add_schedule_role_form.date_time_session.data,
                                          name_role=add_schedule_role_form.role_in_play.data,
                                          name_play=add_schedule_role_form.name_session.data,
                                          stage_year=play_for_info.stage_year)

            try:
                db.session.add(role_for_schedule)
                db.session.commit()
            except:
                DbErrorAdd()

            return redirect(url_for('schedule'))

        else:
            return render_template('schedule.html', schedule=tabletop, roles=roles, session_form=session_form,
                                   role_form=role_form, add_session_form=add_session_form,
                                   add_schedule_role_form=add_schedule_role_form)

    # Отображение страницы с расписанием без функционала
    elif session['role'] is not None:

        tabletop = db.session.query(Schedule).all()
        roles = db.session.query(ActorRole).all()

        return render_template('schedule.html', schedule=tabletop, roles=roles)

    else:
        return redirect(url_for('home_page'))


# Маршрут с логикой организации регистрации на сайте через форму с ошибками и добавлением в БД
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    # Проверка нажатия кнопки "Создать аккаунт"
    if form.validate_on_submit():
        # Заполнение введённых данных о пользователе
        user_to_create = Employee(username=form.username.data, fio=form.fio.data,
                                  birthday=form.birthday.data, mobile_number=form.mobile_number.data,
                                  home_phone_number=form.home_phone_number.data, adress=form.adress.data,
                                  password=form.password1.data)

        # Механизм добавления нового пользователя в базу
        try:
            db.session.add(user_to_create)
            db.session.commit()
        except:
            DbErrorAdd()
            return redirect(url_for('register_page'))

        return redirect(url_for('login_page'))

    # Механизм вывода ошибок при создании нового пользователя
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка при создании нового пользователя: {err_msg}', category='danger')

    return render_template('register.html', form=form)


# Маршрут с логикой авторизации на сайте с обращением к таблице пользователей в БД
# При успешном входе в переменной session сохраняется идентификатор должности пользователя
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # Проверка нажатия на клавишу "Вход"
    if form.validate_on_submit():
        attempted_user = db.session.query(Employee).filter_by(username=form.username.data).first()
        # Проверка на наличие пользователя в базе
        if attempted_user:
            # Проверка на совпадение введённого пароля и пароля в базе
            if form.password.data in attempted_user.password:
                login_user(attempted_user)
                flash(f'Вход выполнен успешно! Вы зашли как {attempted_user.username}', category='success')
                session['role'] = attempted_user.id_position
            else:
                flash('Пароль неверный! Попробуйте снова', category='danger')

            return redirect(url_for('home_page'))
        else:
            flash('Логин не найден! Попробуйте снова', category='danger')

    return render_template('login.html', form=form)


# Маршрут с логикой выхода из аккаунта на сайте - организован через flask_login, который выходит из сессии
# Обнуление переменной session['role'] и возвращение на главную страницу
@app.route('/logout')
def logout_page():
    logout_user()
    session.pop('role', None)
    flash("Вы вышли из аккаунта", category='info')
    return redirect(url_for('home_page'))
