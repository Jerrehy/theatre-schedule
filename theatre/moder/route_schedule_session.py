from flask import render_template, redirect, url_for, session, Blueprint, request
from theatre.models import PlayInfo, Schedule
from theatre.forms import ChangeSession, AddSession
from flask_login import login_required

route_schedule_session = Blueprint('route_schedule_session', __name__, template_folder="templates")


@route_schedule_session.route('/schedule_session', methods=['GET', 'POST'])
@login_required
def schedule_session():
    if session['role'] == 7:
        # Подключение таблиц с общим расписанием сеансов и расписанием для сотрудников
        tabletop = Schedule.get_schedule()
        plays = PlayInfo.get_all_play_info()

        # Добавление форм для добавления сеанса и позиции в расписании сотрудников
        add_session_form = AddSession()
        session_form = ChangeSession()

        # Выпадающие списки для удаления и редактирования расписания сеансов
        session_form.session_name.choices = list(set([i.name_play for i in tabletop]))

        change_info_for_form = Schedule.get_all_schedule_by_name_play(session_form.session_name.choices[0])

        session_form.stage_year.choices = list(set([i.stage_year for i in change_info_for_form]))
        session_form.date_time_session.choices = list(set([i.date_and_time for i in change_info_for_form]))
        session_form.hall_number.choices = list(set([i.hall_number for i in change_info_for_form]))

        # Выпадающий список доступных постановок
        add_session_form.name_session.choices = list(set([i.name_play for i in plays]))

        plays_for_add_form = PlayInfo.get_all_play_info_by_name_play(add_session_form.name_session.choices[0])
        add_session_form.stage_year_session.choices = list(set([i.stage_year for i in plays_for_add_form]))

        if request.method == "POST":
            # Метод удаления сеанса спектакля из расписания
            if session_form.submit_del_ses.data:
                Schedule.delete_schedule(session_form.session_name.data, session_form.date_time_session.data,
                                         session_form.hall_number.data)
                return redirect(url_for('route_schedule_session.schedule_session'))

            # Метод добавления нового сеанса спектакля в расписание театра
            elif add_session_form.submit_add_play.data:

                Schedule.add_schedule_position(add_session_form.date_time_session.data,
                                               add_session_form.hall_number.data,
                                               add_session_form.type_session.data, add_session_form.name_session.data,
                                               add_session_form.stage_year_session.data)

                return redirect(url_for('route_schedule_session.schedule_session'))

            else:
                # Заполнение списка года постановки спектакля для добавления нового сеанса
                if add_session_form.name_session.data:

                    plays_for_add_form = PlayInfo.get_all_play_info_by_name_play(add_session_form.name_session.data)
                    add_session_form.stage_year_session.choices = list(set([i.stage_year for i in plays_for_add_form]))

                # Заполнение списка выбора года постановки и даты проведения сеанса для удаления
                elif session_form.session_name.data:

                    session_form.stage_year.choices = \
                        list(set([i.stage_year for i in tabletop
                                  if i.name_play == session_form.session_name.data]))

                    session_form.date_time_session.choices = \
                        list(set([i.date_and_time for i in tabletop
                                  if i.name_play == session_form.session_name.data]))

                    session_form.hall_number.choices = list(set([i.hall_number for i in tabletop
                                                                 if i.name_play == session_form.session_name.data]))

                return render_template('schedule_session.html', schedule=tabletop, session_form=session_form,
                                       add_session_form=add_session_form)
        else:
            return render_template('schedule_session.html', schedule=tabletop, session_form=session_form,
                                   add_session_form=add_session_form)

    # Если не модератор зашёл в этот узел, то весь функционал недоступен
    elif session['role'] is not None:
        tabletop = Schedule.get_schedule()
        return render_template('schedule_session.html', schedule=tabletop)

    else:
        return redirect(url_for('user.home_page'))
