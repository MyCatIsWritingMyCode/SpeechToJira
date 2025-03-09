import logging
from transformers import pipeline
from models.app_config import *

class SpeechToText:
    def __init__(self, logger : logging.Logger, config : Config):
        self.logger = logger
        self.config : Config = config

        try:
            self.transcriber = pipeline("automatic-speech-recognition", model=config.model_config.tts_model, return_timestamps=True, language='en')
            self.logger.info(f"Initialized speech-to-text model: {config.model_config.tts_model}")
        except Exception as e:
            self.logger.error(f"Failed to initialize speech-to-text model: {e}")
            raise

    def transcribe(self, audio_file : str) -> str:
        try:
            text = self.transcriber(audio_file)["text"]
            return text
        except Exception as e:
            self.logger.error(f"Transcription failed for {audio_file}: {e}")
            raise