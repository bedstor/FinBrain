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
                text += page.extract_text()
        return text
    
    def parse(self):
        """Берём текст со страниц и вызываем метод для обработки его"""
        raw_text = self._get_raw_text()
        return self._process_text(raw_text)

    def _process_text(self, text):
        """Обрабатываем текст"""
        pass


class TBankParser(BaseBankParser):
    """Модель Т-банка"""

    def _process_text(self, text: str) -> list:
        """
        Разрезаем текст на строки
        """
        lines = text.split("\n")
        pattern = r"(?P<date>^\d{2}\.\d{2}\.\d{4})\s(?P<category>[А-Яа-яA-Za-z]+)\s"
        pattern += r"(?P<sum>[+-]?\d+\.\d{2})\s(?P<description>\D[А-Яа-яA-Za-z]+$)"
        result = []
        for line in lines:
            match = re.match(pattern, line)
            if not match:
                continue # Если None - пропускаем строку
            transaction_dict = match.groupdict()
            result.append(transaction_dict)
                
        return result
            

parser = TBankParser("data/test_bank.pdf")
print(parser.parse())




