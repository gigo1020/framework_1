import random


class CreditFactory:
    @staticmethod
    def invalid_account_id() -> int:
        """Генерирует случайный несуществующий account_id для тестов"""
        return random.randint(101, 10000)

    @staticmethod
    def invalid_credit_id() -> int:
        """Генерирует случайный несуществующий credit_id для тестов"""
        return random.randint(101, 10000)

    @staticmethod
    def insufficient_amount(original_amount: float | int) -> float | int:
        """Генерирует случайную сумму, превышающую доступные средства, чтобы вызвать ошибку недостатка средств"""
        return original_amount + random.randint(100, 5000)

    @staticmethod
    def invalid_amount() -> float:
        """Генерирует случайную не положительную сумму для тестов"""
        return round(random.uniform(-15000, 0), 2)

    @staticmethod
    def amount_less_than_minimum() -> int:
        """Генерирует случайную сумму меньше минимальной для тестов"""
        return random.randint(1, 4999)

    @staticmethod
    def amount_greater_than_maximum() -> int:
        """Генерирует случайную сумму больше максимальной для тестов"""
        return random.randint(15001, 65000)
