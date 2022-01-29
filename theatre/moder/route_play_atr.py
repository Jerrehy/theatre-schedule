from flask import render_template, redirect, url_for, session, Blueprint
from theatre.models import Genre, Author
from theatre.forms import DeleteAuthor, DeleteGenre, AddAuthor, AddGenre
from flask_login import login_required

# Создание узла для обращения к атрибутам спектакля
route_play_atr = Blueprint('route_play_atr', __name__, template_folder="templates")


@route_play_atr.route('/play-atr', methods=['GET', 'POST'])
@login_required
def play_atr():
    if session['role'] == 7:
        # Форма для удаления автора
        delete_author_form = DeleteAuthor()
        # Форма для удаления жанра
        delete_genre_form = DeleteGenre()

        # Форма добавления нового жанра
        add_genre_form = AddGenre()
        # Форма добавления нового автора
        add_author_form = AddAuthor()

        # Обращение к базе за списком всех доступных авторов и жанров
        available_genres = Genre.get_genre()
        available_authors = Author.get_author()

        # Заполнение select поля для формы удаления автора: ФИО
        delete_author_form.author_fio.choices = [i.author_fio for i in available_authors]

        birthdays_for_form = Author.get_all_author_birthday_year_by_fio(delete_author_form.author_fio.choices[0])

        # Заполнение select поля для формы удаления автора: Год рождения
        delete_author_form.author_birthday.choices = [i.author_birthday_year for i in birthdays_for_form]

        # Заполнение select поля для формы удаления жанра
        delete_genre_form.genre_name.choices = [i.genre_name for i in available_genres]

        # Метод удаления автора
        if delete_author_form.submit_del_author.data:
            Author.delete_author(delete_author_form.author_fio.data)
            return redirect(url_for('route_play_atr.play_atr'))

        # Метод удаления жанра
        elif delete_genre_form.validate_on_submit():
            Genre.delete_genre(delete_genre_form.genre_name.data)
            return redirect(url_for('route_play_atr.play_atr'))

        # Метод добавления нового автора
        elif add_author_form.validate_on_submit():
            Author.add_author(add_author_form.author_fio.data, add_author_form.author_birthday_year.data)
            return redirect(url_for('route_play_atr.play_atr'))

        # Метод добавления нового жанра
        elif add_genre_form.validate_on_submit():
            Genre.add_genre(add_genre_form.genre_name.data)
            return redirect(url_for('route_play_atr.play_atr'))

        # Заполнение формы для удаления авторов: Год рождения автора
        elif delete_author_form.author_fio.data:
            birthdays_for_form = Author.get_all_author_birthday_year_by_fio(delete_author_form.author_fio.data)
            delete_author_form.author_birthday.choices = [i.author_birthday_year for i in birthdays_for_form]

        # Возвращение шаблона html с полной информацией об атрибутах спектакля
        return render_template('play-atr.html', authors=available_authors, genres=available_genres,
                               delete_author_form=delete_author_form, delete_genre_form=delete_genre_form,
                               add_genre_form=add_genre_form, add_author_form=add_author_form)
    else:
        redirect(url_for('user.home_page'))
