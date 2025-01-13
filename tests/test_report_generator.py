import os
import pytest
from unittest.mock import patch, mock_open
from flask_payroll.views.report_generator import ReportGeneratorFactory, ReportFormat, CSVReportGenerator, JSONReportGenerator
from .controllers.payroll import Payroll
from flask_payroll.models.hourly_employee import HourlyEmployee
from flask_payroll.models.salaried_employee import SalariedEmployee

EXPORT_DIR = "tests/export"
os.makedirs(EXPORT_DIR, exist_ok=True)

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

def test_csv_report_generation(payroll_with_data):
    report_generator = ReportGeneratorFactory.get_report_generator(ReportFormat.CSV)
    report_filename = os.path.join(EXPORT_DIR, "test_payroll_report.csv")
    report_generator.save_report(payroll_with_data, report_filename)
    assert os.path.exists(report_filename)

def test_json_report_generation(payroll_with_data):
    report_generator = ReportGeneratorFactory.get_report_generator(ReportFormat.JSON)
    report_filename = os.path.join(EXPORT_DIR, "test_payroll_report.json")
    report_generator.save_report(payroll_with_data, report_filename)
    assert os.path.exists(report_filename)

def test_report_generator_factory():
    assert isinstance(ReportGeneratorFactory.get_report_generator(ReportFormat.CSV), CSVReportGenerator)
    assert isinstance(ReportGeneratorFactory.get_report_generator(ReportFormat.JSON), JSONReportGenerator)
    with pytest.raises(ValueError):
        ReportGeneratorFactory.get_report_generator("InvalidFormat")

def test_csv_report_generation_empty_payroll():
    payroll = Payroll()
    report_generator = ReportGeneratorFactory.get_report_generator(ReportFormat.CSV)
    report_filename = os.path.join(EXPORT_DIR, "test_payroll_report_empty.csv")
    report_generator.save_report(payroll, report_filename)
    assert os.path.exists(report_filename)

def test_json_report_generation_empty_payroll():
    payroll = Payroll()
    report_generator = ReportGeneratorFactory.get_report_generator(ReportFormat.JSON)
    report_filename = os.path.join(EXPORT_DIR, "test_payroll_report_empty.json")
    report_generator.save_report(payroll, report_filename)
    assert os.path.exists(report_filename)