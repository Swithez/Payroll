import csv
import json
from enum import Enum
from abc import ABC, abstractmethod

# Абстрактный класс для генераторов отчетов
class ReportGenerator(ABC):
    def generate_report(self, payroll):
        # Common steps for all reports
        self.print_header()
        self.print_employee_data(payroll)
        self.print_footer(payroll)

    def generate_report(self, payroll):
        # Общие шаги для всех отчетов
        self.print_header()
        self.print_employee_data(payroll)
        self.print_footer(payroll)

    def print_header(self):
        raise NotImplementedError

    def print_employee_data(self, payroll):
        for employee in payroll.employees:
            print(f"{employee.name} (ID: {employee.employee_id}): {employee.calculate_salary()} USD")

    def print_footer(self, payroll):
        print("----------------------")
        print(f"Total Payroll: {payroll.calculate_total_payroll()} USD")
        print(f"Average Salary: {payroll.get_average_salary():.2f} USD")
    
    @abstractmethod
    def save_report(self, payroll, filename):
        pass

# Перечисление форматов отчётов
class ReportFormat(Enum):
    CSV = "csv"
    JSON = "json"

# Генерация отчёта в веб
class ReportGeneratorFactory:

    @staticmethod
    def get_report_generator(format_type: ReportFormat):
        if format_type == ReportFormat.CSV:
            return CSVReportGenerator()
        elif format_type == ReportFormat.JSON:
            return JSONReportGenerator()
        else:
            raise ValueError(f"Unsupported report format: {format_type}")

# Конкретный класс для генерации отчета в формате CSV
class CSVReportGenerator(ReportGenerator):
    def print_header(self):
        print("Payroll Report (CSV)")
        print("----------------------")
    
    def save_report(self, payroll, filename="data/export/payroll_report.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            stats = payroll.get_statistics()
            writer.writerow(["Суммарная заработная плата", stats["Суммарная заработная плата"]])
            writer.writerow(["Средняя заработная плата", stats["Средняя заработная плата"]])
            writer.writerow(["Медианная заработная плата", stats["Медианная заработная плата"]])
            writer.writerow(["Минимальная заработная плата", stats["Минимальная заработная плата"]])
            writer.writerow(["Максимальная заработная плата", stats["Максимальная заработная плата"]])
            writer.writerow([])  # Пустая строка для разделения
            writer = csv.writer(file)
            writer.writerow(["Name", "Employee ID", "Salary"])
            for employee in payroll.employees:
                writer.writerow([employee.name, employee.employee_id, employee.calculate_salary()])
        print(f"Report saved to {filename}")

# Конкретный класс для генерации отчета в формате JSON
class JSONReportGenerator(ReportGenerator):
    def print_header(self):
        print("Payroll Report (JSON)")
        print("----------------------")

    def save_report(self, payroll, filename="data/export/payroll_report.json"):
        data = {
            "employees": [employee.to_dict() for employee in payroll.employees], # Используем to_dict()
            "statistics": payroll.get_statistics(),
            "total_payroll": payroll.calculate_total_payroll(),
            "average_salary": payroll.get_average_salary(),
        }
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False) # ensure_ascii=False для корректного отображения кириллицы
        print(f"Report saved to {filename}")