from flask import render_template, redirect, url_for, session, Blueprint
from theatre.models import ActorRole
from flask_login import login_required, current_user

# Создание узла для обращения к личному расписанию
employee_schedule = Blueprint('employee_schedule', __name__, template_folder="templates")


# Вывод личного расписания пользователя (не администратора и не модератора)
@employee_schedule.route('/personal_schedule_employee', methods=['GET', 'POST'])
@login_required
def personal_schedule_employee():
    # Проверка, что сотрудник не админ и не модератор
    if session['role'] != 7 and session['role'] != 8:
        # Получение расписания пользователя из базы данных
        roles = ActorRole.get_actor_role_by_id(current_user.get_id())
        # Вывод шаблона html с расписанием пользователя
        return render_template('personal_schedule_employee.html', roles=roles)
    else:
        return redirect(url_for('user.home_page'))
