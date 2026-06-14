import pdfplumber

class BaseBankParser:
    """Стандартная модель банка"""

    def __init__(self, file_path: str):
        """Инициализируем атрибуты класса: путь к файлу"""
        self.file_path = file_path

    def _get_raw_text(self):
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
    """"""
    




