from .employee import Employee

class HourlyEmployee:
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        self.name = name
        self.employee_id = employee_id
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked

    def to_dict(self):
        return {
            "name": self.name,
            "employee_id": self.employee_id,
            "hourly_rate": self.hourly_rate,
            "hours_worked": self.hours_worked,
            "type": "Почасовая оплата"
        }

    def __repr__(self):
        return f"HourlyEmployee(name='{self.name}', id={self.employee_id}, rate={self.hourly_rate}, hours={self.hours_worked})"