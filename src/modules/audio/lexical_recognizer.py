class LexicalRecognizer:
    def recognize(self, tokens):
        print("[LexicalRecognizer] Recognizing lexemes...")
        # In real system: use NLP model
        return [token.lower() for token in tokens]