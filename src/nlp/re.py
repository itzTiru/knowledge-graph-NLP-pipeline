import spacy

class RelationExtractor:
    def __init__(self, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Spacy model 404")
            raise

    def extract_relations(self, text, entities):
        doc = self.nlp(text)
        relations = []

        if len(entities) < 2:
            return []

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                ent1 = entities[i]
                ent2 = entities[j]
                root = None
                for token in doc:
                    if token.dep_ == "ROOT" and token.pos_ == "VERB":
                        root = token.lemma_
                        break
                
                if root:
                    relation = root.upper()
                else:
                    relation = "RELATED_TO"
                
                relations.append((ent1['word'], relation, ent2['word']))
                
        return relations
