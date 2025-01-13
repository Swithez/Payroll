from .employee import Employee

# Класс для представления почасового сотрудника.
class HourlyEmployee:
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        self.name = name
        self.employee_id = employee_id
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    # Рассчитывает заработную плату почасового сотрудника.
    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked

    # Преобразует данные почасового сотрудника в словарь.
    def to_dict(self):
        return {
            "name": self.name,
            "employee_id": self.employee_id,
            "hourly_rate": self.hourly_rate,
            "hours_worked": self.hours_worked,
            "type": "Почасовая оплата"
        }

    #  Представляет объект HourlyEmployee в читаемом виде для удобства отладки.
    def __repr__(self):
        return f"HourlyEmployee(name='{self.name}', id={self.employee_id}, rate={self.hourly_rate}, hours={self.hours_worked})"
