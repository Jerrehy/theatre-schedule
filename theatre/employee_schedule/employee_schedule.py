from flask import render_template, redirect, url_for, session, Blueprint
from theatre.models import ActorRole
from flask_login import login_required, current_user

employee_schedule = Blueprint('employee_schedule', __name__, template_folder="templates")


@employee_schedule.route('/personal_schedule_employee', methods=['GET', 'POST'])
@login_required
def personal_schedule_employee():
    if session['role'] != 7 and session['role'] != 8:
        roles = ActorRole.get_actor_role_by_id(current_user.get_id())
        return render_template('personal_schedule_employee.html', roles=roles)
    else:
        return redirect(url_for('user.home_page'))
