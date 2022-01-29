from flask import render_template, redirect, url_for, session, Blueprint, request
from theatre.models import Genre, Author, PlayInfo
from theatre.forms import ChangePlay, AddPlay
from flask_login import login_required

# Создание узла для обращения к спектаклям, которые ставятся в театре
route_play_info = Blueprint('route_play_info', __name__, template_folder="templates")


@route_play_info.route('/play-info', methods=['GET', 'POST'])
@login_required
def play_info():
    if session['role'] == 7:
        # Форма для удаления спектакля из репертуара
        change_play_form = ChangePlay()
        # Форма добавления нового спектакля в репертуар
        add_play_form = AddPlay()

        # Получение данных из БД про доступные спектакли, жанры и авторов
        available_plays = PlayInfo.get_all_play_info()
        available_authors = Author.get_author()
        available_genres = Genre.get_genre()

        # Заполнение select поля с названием спектаклей для формы удаления
        change_play_form.name_play.choices = list(set([i.name_play for i in available_plays]))

        # Заполнение select поля дата постановки спектакля для формы удаления
        date_for_change_form = PlayInfo.get_all_play_info_by_name_play(change_play_form.name_play.choices[0])
        change_play_form.stage_year.choices = [i.stage_year for i in date_for_change_form]

        # Заполнение select поля со списком авторов из БД
        add_play_form.author_fio.choices = list(set([i.author_fio for i in available_authors]))

        # Заполнение select поля со списком жанров из БД
        add_play_form.genre_name.choices = [i.genre_name for i in available_genres]

        # Заполнение select поля со списком годов рождения автора
        birthdays = Author.get_all_author_birthday_year_by_fio(add_play_form.author_fio.choices[0])
        add_play_form.author_birthday.choices = list(set([i.author_birthday_year for i in birthdays]))

        # Удаление спектаклей в театре
        if change_play_form.submit_del_play.data:
            PlayInfo.delete_play_info_by_name_and_stage_year(change_play_form.name_play.data,
                                                             change_play_form.stage_year.data)
            return redirect(url_for('route_play_info.play_info'))

        # Добавление нового спектакля
        elif add_play_form.submit_add_play.data:
            PlayInfo.add_play_info(add_play_form.name_play.data, add_play_form.stage_year.data,
                                   add_play_form.acts_number.data, add_play_form.discription.data,
                                   add_play_form.genre_name.data, add_play_form.author_fio.data,
                                   add_play_form.author_birthday.data)

        # Заполнение списка дней рождения при совпадении авторов при изменении select поля с ФИО автора
        elif add_play_form.author_fio.data:
            birthdays = Author.get_all_author_birthday_year_by_fio(add_play_form.author_fio.data)
            add_play_form.author_birthday.choices = list(set([i.author_birthday_year for i in birthdays]))

        # Заполнение списка дат при изменении select поля с именем спектакля
        elif change_play_form.name_play.data:
            date_for_change_form = PlayInfo.get_all_play_info_by_name_play(change_play_form.name_play.data)
            change_play_form.stage_year.choices = list(set([i.stage_year for i in date_for_change_form]))

        return render_template('play-info.html', plays=available_plays, change_play_form=change_play_form,
                               add_play_form=add_play_form)

    else:
        return redirect(url_for('user.home_page'))
