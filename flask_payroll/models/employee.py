from abc import ABC, abstractmethod

# Абстрактный базовый класс для сотрудников.
class Employee(ABC):
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    # Абстрактный метод для расчета заработной платы.
    @abstractmethod
    def calculate_salary(self):
        pass

    # Абстрактный метод для преобразования данных сотрудника в словарь.
    @abstractmethod
    def to_dict(self):
        pass
