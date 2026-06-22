import pdfplumber
import re

class BankParserFactory:
    """Фабрика, которая сама определяет банк и запускает парсера"""

    def __init__(self, file_path: str):
        """Инициализируем атрибуты класса: путь к файлу"""
        self.file_path = file_path
    
    def get_parse(self):
        """Определяем банк и возвращаем объект этого банка"""
        base = BaseBankParser(self.file_path)
        raw_text = base._get_raw_text()
        ALL_BANKS = [TBankParser, SberParser] # Все существующие банки
        for bank in ALL_BANKS:
            for marker in bank.BANK_MARKERS:
                if marker in raw_text:
                    return bank(self.file_path)
    
        # Если ничего не нашлось - значит, банк неизвестен
        return AIBankParser(self.file_path)


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

    # Слова-маркеры, по которым можно отличить Т-банк
    BANK_MARKERS = ["Т-Банк", "Т-БАНК", "T-Bank", "Тинькофф", "Tinkoff"]

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

    # Слова-маркеры, по которым можно отличить Сбербанк
    BANK_MARKERS = ["Сбербанк", "СБЕРБАНК", "Sberbank", "SBERBANK"]

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


class AIBankParser(BaseBankParser):
    """Модель ИИ-банка"""
    
    def _process_text(self, text: str):
        """
        Отправялем сырой текст в ассинхронную функцию и получаем готовый список словарей
        """

        print("Включаю ИИ-распознавание текста...")
        return []

factory = BankParserFactory("data/sber_bank_test.pdf")
parser = factory.get_parse()
print(parser.parse())

