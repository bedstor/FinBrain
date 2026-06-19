import pdfplumber
import re

class BaseBankParser:
    """Стандартная модель банка"""

    def __init__(self, file_path: str):
        """Инициализируем атрибуты класса: путь к файлу"""
        self.file_path = file_path

    def _get_raw_text(self) -> str:
        """Получение и сохранение сырого текста со страниц файла"""
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted: # Проверяем, что текст успешно считался
                    text += extracted + "\n"

        return text
    
    def parse(self):
        """Берём текст со страниц и вызываем метод для обработки его"""
        raw_text = self._get_raw_text()
        return self._process_text(raw_text)

    def _process_text(self, text: str) -> list:
        """
        Находим нужные данные по паттерну, группируем
        и возвращаем их в виде пары "ключ - значение"
        """
        pattern = self.make_pattern()
        result = []
        for match in pattern.finditer(text):
            transaction_dict = match.groupdict()
            result.append(transaction_dict)
        
        return result
    
    def make_pattern(self):
        """Предохранитель: заставляет дочерние классы создавать свой паттерн"""
        raise NotImplementedError(
            "Вы забыли создать метод make_pattern в дочернем классе"
)


class TBankParser(BaseBankParser):
    """Модель Т-банка"""

    def make_pattern(self):
        """Создание паттерна для нахождения данных"""

        return re.compile(r"""
            # Дата и время операции
            (?P<date_time>\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2})\s+
            # Дата учета    
            (?P<date_accounting>\d{2}\.\d{2}\.\d{4})\s+
            # Любые символы до начала суммы
            (?P<description_operation>.*?)\s+
            # Сумма с пробелами в тысячах или без них + значок рубля
            (?P<sum_value>[+--—–]?\d+(?:\s\d+)*\.\d{2})\s*₽?\s+
            (?P<remainder>\d+(?:\s\d+)*\.\d{2}\s*₽?)
""", re.VERBOSE | re.MULTILINE) 


class SberParser(BaseBankParser):
    """Модель Сбер-банка"""

    def make_pattern(self):
        """Создание паттерна для нахождения данных"""

        return re.compile(r"""
            # Дата и время операции
            (?P<date_time>\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2})\s+
            # Дата учета    
            (?P<date_accounting>\d{2}\.\d{2}\.\d{4})\s+
            # Любые символы до начала суммы
            (?P<description_operation>.*?)\s+
            # Сумма с пробелами в тысячах или без них + значок рубля
            (?P<sum_value>[+--—–]?\d+(?:\s\d+)*\,\d{2})\s*₽?\s+
            (?P<remainder>\d+(?:\s\d+)*\,\d{2}\s*₽?)
""", re.VERBOSE | re.MULTILINE) 

t_bank = TBankParser("data/t_bank_test.pdf")
sber = SberParser("data/sber_bank_test.pdf")
print(t_bank.parse())
print(sber.parse())

