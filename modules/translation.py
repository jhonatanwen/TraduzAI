from transformers import MarianMTModel, MarianTokenizer


class Translator:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-ja-pt"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            outputs = self.model.generate(**inputs)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise RuntimeError(f"Erro na tradução: {str(e)}")