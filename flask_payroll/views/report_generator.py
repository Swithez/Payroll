import csv
import json
from enum import Enum
from abc import ABC, abstractmethod

# Абстрактный класс для генераторов отчетов
class ReportGenerator(ABC):
    # Генерирует отчет, выполняя общие шаги
    def generate_report(self, payroll):
        self.print_header()
        self.print_employee_data(payroll)
        self.print_footer(payroll)

    # Абстрактный метод для вывода заголовка отчета.
    def print_header(self):
        raise NotImplementedError

    # Выводит данные о сотрудниках на экран.
    def print_employee_data(self, payroll):
        for employee in payroll.employees:
            print(f"{employee.name} (ID: {employee.employee_id}): {employee.calculate_salary()} USD")

    # Выводит подвал отчета (общая зарплата, средняя зарплата).
    def print_footer(self, payroll):
        print("----------------------")
        print(f"Total Payroll: {payroll.calculate_total_payroll()} USD")
        print(f"Average Salary: {payroll.get_average_salary():.2f} USD")

    # Абстрактный метод для сохранения отчета в файл.
    @abstractmethod
    def save_report(self, payroll, filename):
        pass

# Перечисление форматов отчётов.
class ReportFormat(Enum):
    CSV = "csv"
    JSON = "json"

# Фабрика генераторов отчётов.
class ReportGeneratorFactory:

    # Фабрика для создания генераторов отчетов.
    @staticmethod
    def get_report_generator(format_type: ReportFormat):
        if format_type == ReportFormat.CSV:
            return CSVReportGenerator()
        elif format_type == ReportFormat.JSON:
            return JSONReportGenerator()
        else:
            raise ValueError(f"Unsupported report format: {format_type}")

# Класс для генерации отчета в формате CSV
class CSVReportGenerator(ReportGenerator):
    # Генератор отчетов в формате CSV.
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

# Класс для генерации отчета в формате JSON
class JSONReportGenerator(ReportGenerator):
    # Генератор отчетов в формате JSON.
    def print_header(self):
        print("Payroll Report (JSON)")
        print("----------------------")

    # Сохраняет отчет в формате JSON в файл.
    def save_report(self, payroll, filename="data/export/payroll_report.json"):
        data = {
            "employees": [employee.to_dict() for employee in payroll.employees], 
            "statistics": payroll.get_statistics(),
            "total_payroll": payroll.calculate_total_payroll(),
            "average_salary": payroll.get_average_salary(),
        }
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Report saved to {filename}")
