from flask import render_template, redirect, url_for, session, Blueprint
from theatre.models import Genre, Author
from theatre.forms import DeleteAuthor, DeleteGenre, AddAuthor, AddGenre
from flask_login import login_required

route_play_atr = Blueprint('route_play_atr', __name__, template_folder="templates")


@route_play_atr.route('/play-atr', methods=['GET', 'POST'])
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
        available_genres = Genre.get_genre()
        available_authors = Author.get_author()

        delete_author_form.author_fio.choices = [i.author_fio for i in available_authors]
        delete_genre_form.genre_name.choices = [i.genre_name for i in available_genres]

        # Метод удаления автора
        if delete_author_form.validate_on_submit():
            Author.delete_author(delete_author_form.author_fio.data)
            return redirect(url_for('moder.play_atr'))

        # Метод удаления жанра
        elif delete_genre_form.validate_on_submit():
            Genre.delete_genre(delete_genre_form.genre_name.data)
            return redirect(url_for('moder.play_atr'))

        # Метод добавления нового автора
        elif add_author_form.validate_on_submit():
            Author.add_author(add_author_form.author_fio.data, add_author_form.author_birthday_year.data)
            return redirect(url_for('moder.play_atr'))

        # Метод добавления нового жанра
        elif add_genre_form.validate_on_submit():
            Genre.add_genre(add_genre_form.genre_name.data)
            return redirect(url_for('moder.play_atr'))

        return render_template('play-atr.html', authors=available_authors, genres=available_genres,
                               delete_author_form=delete_author_form, delete_genre_form=delete_genre_form,
                               add_genre_form=add_genre_form, add_author_form=add_author_form)
    else:
        redirect(url_for('user.home_page'))
