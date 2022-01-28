from flask import render_template, redirect, url_for, session, Blueprint, request
from theatre.models import PlayInfo, Employee, Schedule, ActorRole
from theatre.forms import RoleEmployee, AddRoleSchedule
from flask_login import login_required

route_schedule_employee = Blueprint('route_schedule_employee', __name__, template_folder="templates")


@route_schedule_employee.route('/schedule_employee', methods=['GET', 'POST'])
@login_required
def schedule_employee():
    if session['role'] == 7:

        roles = ActorRole.get_actor_role()
        tabletop = Schedule.get_schedule()
        employers = Employee.get_employee()

        add_schedule_role_form = AddRoleSchedule()
        role_form = RoleEmployee()

        role_form.session_name.choices = list(set([i.name_play for i in roles]))

        role_info_for_form = ActorRole.get_actor_role_by_name_play(name_play=role_form.session_name.choices[0])

        role_form.stage_year.choices = list(set([i.stage_year for i in role_info_for_form]))
        role_form.date_time_session.choices = list(set([i.date_and_time for i in role_info_for_form]))
        role_form.employee_fio.choices = list(set([i.employee.fio for i in role_info_for_form]))

        add_schedule_role_form.name_session.choices = list(set([i.name_play for i in tabletop]))
        add_schedule_role_form.actor.choices = list(set([i.fio for i in employers if i.id_position
                                                         and i.id_position != 7 and i.id_position != 8]))

        schedule_info_for_form = Schedule.get_all_schedule_by_name_play(add_schedule_role_form.name_session.choices[0])

        add_schedule_role_form.stage_year_session.choices = list(set([i.stage_year for i in schedule_info_for_form]))
        add_schedule_role_form.date_time_session.choices = list(set([i.date_and_time for i in schedule_info_for_form]))

        if request.method == 'POST':
            if role_form.submit_del_role.data:

                my_employee = Employee.get_employee_by_fio(role_form.employee_fio.data)
                ActorRole.delete_actor_role_position(role_form.session_name.data, role_form.date_time_session.data,
                                                     my_employee.personal_number)
                return redirect(url_for('route_schedule_employee.schedule_employee'))

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

            elif role_form.session_name.data:
                roles_name_session = ActorRole.get_actor_role_by_name_play(role_form.session_name.data)

                role_form.stage_year.choices = list(set([i.stage_year for i in roles_name_session]))
                role_form.date_time_session.choices = list(set([i.date_and_time for i in roles_name_session]))
                role_form.employee_fio.choices = list(set([i.employee.fio for i in roles_name_session]))

            elif add_schedule_role_form.name_session.data:

                roles_name_session = Schedule.get_all_schedule_by_name_play(add_schedule_role_form.name_session.data)

                add_schedule_role_form.stage_year_session.choices = list(set(
                                                                    [i.stage_year for i in roles_name_session]))

                add_schedule_role_form.date_time_session.choices = list(set(
                                                                    [i.date_and_time for i in roles_name_session]))

            return render_template('schedule_employee.html', roles=roles, role_form=role_form,
                                   add_schedule_role_form=add_schedule_role_form)
        else:
            return render_template('schedule_employee.html', roles=roles, role_form=role_form,
                                   add_schedule_role_form=add_schedule_role_form)

    elif session['role'] is not None:

        roles = ActorRole.get_actor_role()

        return render_template('schedule_employee.html', roles=roles)

    else:
        redirect(url_for('user.home_page'))
