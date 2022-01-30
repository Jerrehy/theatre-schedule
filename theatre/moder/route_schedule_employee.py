from flask import render_template, redirect, url_for, session, Blueprint, request
from theatre.models import EmployeePosition, Employee, Schedule, ActorRole
from theatre.forms import RoleEmployee, AddRoleSchedule
from flask_login import login_required

# Создание узла для обращения к общему расписанию сотрудников
route_schedule_employee = Blueprint('route_schedule_employee', __name__, template_folder="templates")


@route_schedule_employee.route('/schedule_employee', methods=['GET', 'POST'])
@login_required
def schedule_employee():
    if session['role'] == 7:
        # Обращение к БД для получения информации о: расписании сотрудников, расписании сеансов и о сотрудниках в целом
        roles = ActorRole.get_actor_role()
        tabletop = Schedule.get_schedule()
        employers = Employee.get_employee()
        employers_positions = EmployeePosition.get_all_employee_position()
        employers_in_positions = list(set([i.personal_number for i in employers_positions
                                           if i.id_position != 7 and i.id_position != 8]))

        # Форма для добавления позиции в расписание сотрудников
        add_schedule_role_form = AddRoleSchedule()
        # Форма для удаления позиции в расписании сотрудников
        role_form = RoleEmployee()

        # Заполение select поля для названий спектаклей из общего расписания сотрудников
        # Для удаления из него уже существующих позиций
        role_form.session_name.choices = list(set([i.name_play for i in roles]))

        # Обращение к БД по информации о первом списке поля select спектакле
        role_info_for_form = ActorRole.get_actor_role_by_name_play(name_play=role_form.session_name.choices[0])

        # Заполнение select полей года постановки, даты проведения и ФИО сотрудника
        # В соответствии с полученными данными из БД
        role_form.stage_year.choices = list(set([i.stage_year for i in role_info_for_form]))
        role_form.date_time_session.choices = list(set([i.date_and_time for i in role_info_for_form]))
        role_form.employee_fio.choices = list(set([i.employee.fio for i in role_info_for_form]))

        # Заполнение select поля названия спектаклей в постановке для добавления новых сеансов
        add_schedule_role_form.name_session.choices = list(set([i.name_play for i in tabletop]))

        # Заполнение select поля с выбором сотрудников, исключая администраторов и модераторов
        add_schedule_role_form.actor.choices = list(set([i.fio for i in employers
                                                         if i.personal_number in employers_in_positions]))

        # Обращение к БД для получения информации по известному названию спектакля
        schedule_info_for_form = Schedule.get_all_schedule_by_name_play(add_schedule_role_form.name_session.choices[0])

        # Заполнение select полей года постановки и даты (времени) проведения
        # В соответствии с полученными данными из БД
        add_schedule_role_form.stage_year_session.choices = list(set([i.stage_year for i in schedule_info_for_form]))
        add_schedule_role_form.date_time_session.choices = list(set([i.date_and_time for i in schedule_info_for_form]))

        # Метод удаления позиции в расписании сотрудников
        if role_form.submit_del_role.data:
            my_employee = Employee.get_employee_by_fio(role_form.employee_fio.data)
            ActorRole.delete_actor_role_position(role_form.session_name.data, role_form.date_time_session.data,
                                                 my_employee.personal_number)
            return redirect(url_for('route_schedule_employee.schedule_employee'))

        # Метод добавления новой позиции в расписание сотрудников
        elif add_schedule_role_form.submit_add_role.data:
            play_for_info = \
                Schedule.get_schedule_by_name_play_stage_year_datetime(
                    add_schedule_role_form.name_session.data,
                    add_schedule_role_form.stage_year_session.data,
                    add_schedule_role_form.date_time_session.data)

            actor_for_info = Employee.get_employee_by_fio(add_schedule_role_form.actor.data)

            ActorRole.add_actor_role(actor_for_info.personal_number, play_for_info.hall_number,
                                     add_schedule_role_form.date_time_session.data,
                                     add_schedule_role_form.role_in_play.data,
                                     add_schedule_role_form.name_session.data, play_for_info.stage_year)

            return redirect(url_for('route_schedule_employee.schedule_employee'))

        # Обновление полей: год постановки спектакля, время проведения сеансов и принимающие участие сотрудник
        # В форме удаления позиции в соотвествии с полученными данными из формы
        elif role_form.session_name.data:
            roles_name_session = ActorRole.get_actor_role_by_name_play(role_form.session_name.data)

            role_form.stage_year.choices = list(set([i.stage_year for i in roles_name_session]))
            role_form.date_time_session.choices = list(set([i.date_and_time for i in roles_name_session]))
            role_form.employee_fio.choices = list(set([i.employee.fio for i in roles_name_session]))

        # Обновление полей: год постановки спектакля и время проведения сеанса
        # В форме добавления новой позиции в расписание в соотвествии с полученными данными из формы
        elif add_schedule_role_form.name_session.data:
            roles_name_session = Schedule.get_all_schedule_by_name_play(add_schedule_role_form.name_session.data)

            add_schedule_role_form.stage_year_session.choices = list(set(
                [i.stage_year for i in roles_name_session]))

            add_schedule_role_form.date_time_session.choices = list(set(
                [i.date_and_time for i in roles_name_session]))

        return render_template('schedule_employee.html', roles=roles, role_form=role_form,
                               add_schedule_role_form=add_schedule_role_form)

    # Если не модератор зашёл в этот узел, то весь функционал недоступен
    elif session['role'] is not None:
        roles = ActorRole.get_actor_role()
        return render_template('schedule_employee.html', roles=roles)

    else:
        redirect(url_for('user.home_page'))
