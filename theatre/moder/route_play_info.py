from flask import render_template, redirect, url_for, session, Blueprint, request
from theatre.models import Genre, Author, PlayInfo
from theatre.forms import ChangePlay, AddPlay
from flask_login import login_required

route_play_info = Blueprint('route_play_info', __name__, template_folder="templates")


@route_play_info.route('/play-info', methods=['GET', 'POST'])
@login_required
def play_info():
    if session['role'] == 7:

        change_play_form = ChangePlay()
        add_play_form = AddPlay()

        available_plays = PlayInfo.get_all_play_info()
        available_authors = Author.get_author()
        available_genres = Genre.get_genre()

        change_play_form.name_play.choices = list(set([i.name_play for i in available_plays]))

        add_play_form.author_fio.choices = list(set([i.author_fio for i in available_authors]))
        add_play_form.genre_name.choices = [i.genre_name for i in available_genres]

        if request.method == 'POST':

            # Удаление спектаклей в театре
            if change_play_form.validate_on_submit():
                PlayInfo.delete_play_info_by_name(change_play_form.name_play.data)
                return redirect(url_for('moder.play_info'))

            # Добавление нового спектакля
            elif add_play_form.validate_on_submit():
                author_birthday_year = Author.get_author_birthday_year_by_fio(add_play_form.author_fio.data)
                PlayInfo.add_play_info(add_play_form.name_play.data, add_play_form.stage_year.data,
                                       add_play_form.acts_number.data, add_play_form.discription.data,
                                       add_play_form.genre_name.data, add_play_form.author_fio.data,
                                       author_birthday_year)
            # Заполнение списка дат
            else:
                change_play_form.stage_year.choices = list(set([i.stage_year for i in available_plays
                                                                if change_play_form.name_play.data == i.name_play]))

                return render_template('play-info.html', plays=available_plays, change_play_form=change_play_form,
                                       add_play_form=add_play_form)

            return redirect(url_for('moder.play_info'))

        else:
            change_play_form.stage_year.choices = list(set([i.stage_year for i in available_plays
                                                            if i.name_play == change_play_form.name_play.choices[0]]))

            return render_template('play-info.html', plays=available_plays, change_play_form=change_play_form,
                                   add_play_form=add_play_form)
    else:
        return redirect(url_for('user.home_page'))
