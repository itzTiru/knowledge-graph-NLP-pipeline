import os
from pypdf import PdfReader
from bs4 import BeautifulSoup

class DocumentLoader:
    def load(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File 404")

        ext = os.path.splitext(file_path)[1].lower()   
        if ext == '.pdf':
            return self._load_pdf(file_path)
        elif ext == '.txt':
            return self._load_text(file_path)
        elif ext in ['.html', '.htm']:
            return self._load_html(file_path)
        else:
            raise ValueError(f"Unsup format{ext}")

    def _load_pdf(self, file_path):
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Err reading{e}")
        return text

    def _load_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text(separator='\n')
