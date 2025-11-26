import spacy
import re

class TextCleaner:
    def __init__(self, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Spacy 404-{model}")
            raise

    def clean(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def split_sentences(self, text):
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]
