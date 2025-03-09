from transformers import pipeline


class DeepSeekNLPProcessor:
    def __init__(self, model_name, logger):
        self.logger = logger
        try:
            self.nlp_model = pipeline("text-classification", model=model_name)
            self.logger.info(f"Initialized NLP processor model: {model_name}")
        except Exception as e:
            self.logger.error(f"Failed to initialize NLP processor model: {e}")
            raise

    def extract_topics(self, text):
        try:
            return [{"title": segment["label"], "content": segment["text"]} for segment in self.nlp_model(text)]
        except Exception as e:
            self.logger.error(f"Topic extraction failed: {e}")
            raise