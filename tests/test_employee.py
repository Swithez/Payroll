import pytest
from flask_payroll.models.hourly_employee import HourlyEmployee
from flask_payroll.models.salaried_employee import SalariedEmployee
from flask_payroll.models.employee import Employee

def test_hourly_employee_creation():
    hourly_employee = HourlyEmployee("Иван", 1, 100, 20)
    assert hourly_employee.name == "Иван"
    assert hourly_employee.employee_id == 1
    assert hourly_employee.hourly_rate == 100
    assert hourly_employee.hours_worked == 20

def test_hourly_employee_calculate_salary():
    hourly_employee = HourlyEmployee("Иван", 1, 100, 20)
    salary = hourly_employee.calculate_salary()
    assert salary == 2000

def test_hourly_employee_to_dict():
    hourly_employee = HourlyEmployee("Иван", 1, 100, 20)
    employee_dict = hourly_employee.to_dict()
    assert employee_dict == {
        "name": "Иван",
        "employee_id": 1,
        "hourly_rate": 100,
        "hours_worked": 20,
        "type": "Почасовая оплата"
    }
def test_hourly_employee_repr():
    hourly_employee = HourlyEmployee("Иван", 1, 100, 20)
    assert repr(hourly_employee) == "HourlyEmployee(name='Иван', id=1, rate=100, hours=20)"

def test_salaried_employee_creation():
    salaried_employee = SalariedEmployee("Петр", 2, 50000)
    assert salaried_employee.name == "Петр"
    assert salaried_employee.employee_id == 2
    assert salaried_employee.annual_salary == 50000

def test_salaried_employee_calculate_salary():
    salaried_employee = SalariedEmployee("Петр", 2, 50000)
    salary = salaried_employee.calculate_salary()
    assert salary == 50000

def test_salaried_employee_to_dict():
    salaried_employee = SalariedEmployee("Петр", 2, 50000)
    employee_dict = salaried_employee.to_dict()
    assert employee_dict == {
        "name": "Петр",
        "employee_id": 2,
        "annual_salary": 50000,
        "type": "Контрактная оплата"
    }

def test_salaried_employee_repr():
    salaried_employee = SalariedEmployee("Петр", 2, 50000)
    assert repr(salaried_employee) == "SalariedEmployee(name='Петр', id=2, salary=50000)"


def test_employee_is_abstract():
    with pytest.raises(TypeError):
        Employee("Test", 1) # Проверка, что нельзя создать экземпляр абстрактного класса