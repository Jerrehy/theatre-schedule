from flask import Blueprint, render_template, redirect, url_for, session
from theatre.models import Employee, Position, EmployeePosition
from theatre.forms import ChangeEmployee
from flask_login import login_required, current_user

# Создание узла для обращению к функциям админа
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
                # Получение данных для обращения к должности сотрудника
                employee_for_update = Employee.get_employee_by_fio(change_form.employee_fio.data)
                id_position_for_update = Position.get_position_id_by_name(change_form.position_name.data)
                id_employee_for_update = employee_for_update.personal_number

                # Изменение должности сотрудника, если она была назначена
                if EmployeePosition.get_employee_position_for_personal_number(id_employee_for_update):
                    EmployeePosition.update_employee_position(id_employee_for_update, id_position_for_update)
                # Добавление должности для нового сотрудника
                else:
                    EmployeePosition.add_employee_position(id_employee_for_update, id_position_for_update)

                return redirect(url_for('admin.employee'))

        # возвращение html шаблона с работниками
        return render_template('employee.html', employers=available_employee, positions=available_position,
                               change_form=change_form)

    else:
        # если пользователь не зарегистрирован, то он попадает на главную страницу
        return redirect(url_for('user.home_page'))
