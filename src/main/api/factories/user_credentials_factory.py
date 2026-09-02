

class UserCredentialsFactory:
    @staticmethod
    def invalid_user_credentials() -> list[tuple[str, str]]:
        """Генерирует список некорректных комбинаций логина и пароля для тестов"""
        return [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abc!", "Pas!sw0rd"),
            ("", ""),
            ("Maxx12", "Паs!sw0рд"),
            ("Maxx13", "sw0rd"),
            ("Maxx14", "pas!sw0rd"),
            ("Maxx15", "PAS!SW0RD"),
            ("Maxx16", "PASSSW0RD"),
            ("Maxx17", "PAS!SWORD"),
        ]