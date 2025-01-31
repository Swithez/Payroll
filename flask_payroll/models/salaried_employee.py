from .employee import Employee

# Класс для представления штатного сотрудника.
class SalariedEmployee:
    def __init__(self, name, employee_id, annual_salary):
        self.name = name
        self.employee_id = employee_id
        self.annual_salary = annual_salary

    # Рассчитывает заработную плату штатного сотрудника.
    def calculate_salary(self):
        return self.annual_salary

    # Преобразует данные штатного сотрудника в словарь.
    def to_dict(self):
        return {
            "name": self.name,
            "employee_id": self.employee_id,
            "annual_salary": self.annual_salary,
            "type": "Контрактная оплата"
        }

    # Представляет объект SalariedEmployee в читаемом виде для удобства отладки.
    def __repr__(self):
        return f"SalariedEmployee(name='{self.name}', id={self.employee_id}, salary={self.annual_salary})"
