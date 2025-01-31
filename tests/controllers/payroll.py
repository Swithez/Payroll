import json
import pandas as pd
from flask_payroll.models.hourly_employee import HourlyEmployee  
from flask_payroll.models.salaried_employee import SalariedEmployee

# Класс для управления ведомостью заработной платы.
class Payroll:
    def __init__(self):
        self.employees = []

    # Добавляет сотрудника в ведомость.
    def add_employee(self, employee):
        self.employees.append(employee)

    # Вычисляет общую сумму заработной платы всех сотрудников.
    def calculate_total_payroll(self):
        return sum(employee.calculate_salary() for employee in self.employees)

    # Вычисляет среднюю заработную плату.
    def get_average_salary(self):
        if not self.employees:
            return 0
        return self.calculate_total_payroll() / len(self.employees)

    # Возвращает список сотрудников заданного типа.
    def get_employees_by_type(self, employee_type):
        return [emp for emp in self.employees if isinstance(emp, employee_type)]

    # Импортирует данные о сотрудниках из JSON-файла.
    def import_employees_from_json(self, file_path):
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                for emp in data:
                    if emp["type"] == "HourlyEmployee":
                        self.add_employee(HourlyEmployee(
                            emp["name"], emp["employee_id"], emp["hourly_rate"], emp["hours_worked"]
                        ))
                    elif emp["type"] == "SalariedEmployee":
                        self.add_employee(SalariedEmployee(
                            emp["name"], emp["employee_id"], emp["annual_salary"]
                        ))
                    else:
                        print(f"Unknown employee type: {emp['type']}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error importing employees: {e}")
        except KeyError as e:
            print(f"Missing key {e} in employee data: {emp}")

    # Вычисляет статистику по заработной плате.
    def get_statistics(self):
        salaries = [employee.calculate_salary() for employee in self.employees]
        if not salaries:  # Проверка на пустой список
            return {
                "Суммарная заработная плата": 0,
                "Средняя заработная плата": 0.0,
                "Медианная заработная плата": 0,
                "Минимальная заработная плата": 0,
                "Максимальная заработная плата": 0,
            }

        df = pd.DataFrame(salaries, columns=["Salary"])
        stats = {
            "Суммарная заработная плата": int(df["Salary"].sum()),
            "Средняя заработная плата": float(df["Salary"].mean()),
            "Медианная заработная плата": int(df["Salary"].median()),
            "Минимальная заработная плата": int(df["Salary"].min()),
            "Максимальная заработная плата": int(df["Salary"].max()),
        }
        return stats

    
