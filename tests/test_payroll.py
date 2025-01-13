import pytest
from unittest.mock import patch, mock_open
from .controllers.payroll import Payroll
from flask_payroll.models.hourly_employee import HourlyEmployee
from flask_payroll.models.salaried_employee import SalariedEmployee


@pytest.fixture
def payroll_with_data():
    payroll = Payroll()
    test_data = [
        {"name": "Иван Иванов", "employee_id": 1, "type": "HourlyEmployee", "hourly_rate": 100, "hours_worked": 160},
        {"name": "Петр Петров", "employee_id": 2, "type": "SalariedEmployee", "annual_salary": 5000},
    ]
    for emp in test_data:
        if emp["type"] == "HourlyEmployee":
            payroll.add_employee(HourlyEmployee(emp["name"], emp["employee_id"], emp["hourly_rate"], emp["hours_worked"]))
        elif emp["type"] == "SalariedEmployee":
            payroll.add_employee(SalariedEmployee(emp["name"], emp["employee_id"], emp["annual_salary"]))
    return payroll

def test_add_employee():
    payroll = Payroll()
    employee = HourlyEmployee("Test Employee", 123, 50, 40)
    payroll.add_employee(employee)
    assert len(payroll.employees) == 1

def test_calculate_total_payroll(payroll_with_data):
    assert payroll_with_data.calculate_total_payroll() == 21000

def test_get_average_salary(payroll_with_data):
    assert payroll_with_data.get_average_salary() == 10500

def test_get_employees_by_type(payroll_with_data):
    hourly_employees = payroll_with_data.get_employees_by_type(HourlyEmployee)
    assert len(hourly_employees) == 1
    assert isinstance(hourly_employees[0], HourlyEmployee)

def test_import_employees_from_json():
    payroll = Payroll()
    mock_json_data = [{'name': 'Test', 'employee_id': 1, 'type': 'HourlyEmployee', 'hourly_rate': 100, 'hours_worked': 10}]
    with patch('builtins.open', mock_open(read_data=str(mock_json_data).replace("'", '"'))): # исправлено
        payroll.import_employees_from_json("fake_path.json")
    assert len(payroll.employees) == 1
    assert isinstance(payroll.employees[0], HourlyEmployee)
    assert payroll.employees[0].name == "Test"

def test_import_employees_from_json_file_not_found():
    payroll = Payroll()
    with patch('builtins.open') as mock_file:
        mock_file.side_effect = FileNotFoundError
        payroll.import_employees_from_json("non_existent_file.json")
    assert len(payroll.employees) == 0

def test_import_employees_from_json_key_error():
    payroll = Payroll()
    mock_json_data = [{'name': 'Test', 'employee_id': 1, 'hourly_rate': 100, 'hours_worked': 10}] #type отсутствует
    with patch('builtins.open', mock_open(read_data=str(mock_json_data).replace("'", '"'))):
        payroll.import_employees_from_json("fake_path.json")
    assert len(payroll.employees) == 0