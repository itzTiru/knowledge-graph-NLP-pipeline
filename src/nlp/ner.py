from transformers import pipeline

class NERExtractor:
    def __init__(self, model_name="dslim/bert-base-NER"):
        self.nlp = pipeline("ner", model=model_name, aggregation_strategy="simple")

    def extract_entities(self, text):
        entities = self.nlp(text)
        return entities
