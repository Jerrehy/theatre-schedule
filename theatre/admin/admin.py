from flask import Blueprint, render_template, redirect, url_for, session
from theatre.models import Employee, Position
from theatre.forms import ChangeEmployee
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__, template_folder="templates")


# Страница с информацией о сотрудниках и их должностях
@admin.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():
    if session['role'] == 8:
        # Подключение формы для изменения информации о сотруднике или для удаления его из базы
        change_form = ChangeEmployee()

        # Извлечение информации о сотрудниках и доступных должностях из базы
        available_employee = Employee.get_employee()
        available_position = Position.get_position()

        # Создание выпадающих списков для вывода доступных сотрудников и доступных позиций
        change_form.position_name.choices = [i.position_name for i in available_position]
        change_form.employee_fio.choices = [i.fio for i in available_employee
                                            if i.personal_number != current_user.get_id()]

        # Метод изменения/удаления сотрудника
        if change_form.validate_on_submit():
            # Удаление сотрудника
            if change_form.submit_del_mpl.data:
                Employee.delete_employee_by_fio(change_form.employee_fio.data)
                return redirect(url_for('admin.employee'))

            # Изменение должности сотрудника
            elif change_form.submit_up_empl.data:
                Employee.update_employee_by_fio(change_form.employee_fio.data, change_form.position_name.data)
                return redirect(url_for('admin.employee'))

        return render_template('employee.html', employers=available_employee, positions=available_position,
                               change_form=change_form)

    else:
        return redirect(url_for('user.home_page'))
