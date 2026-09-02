import random


class DepositFactory:
    @staticmethod
    def boundary_invalid_amounts() -> list[float]:
        """Генерирует список граничных значений для тестов с некорректными суммами"""
        return [
            505.05,
            998.0,
            999.99,  # меньше минимальной суммы
            9000.01,  # больше максимальной суммы
            9001.00,
            14500.00
        ]

    @staticmethod
    def invalid_amount() -> float:
        """Генерирует случайную невалидную сумму для депозита (меньше 1000 или больше 9000)"""
        if random.choice([True, False]):
            return round(random.uniform(0.01, 999.99), 2)  # меньше минимальной суммы
        else:
            return round(random.uniform(9000.01, 20000.00), 2)  # выше максимальной суммы

    @staticmethod
    def empty_auth_headers():
        """ Возвращает пустой словарь для имитации отсутствия авторизационных заголовков"""
        return {}
