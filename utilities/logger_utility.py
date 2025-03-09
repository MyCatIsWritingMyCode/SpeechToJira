import logging
from models.app_config import LogConfig
from datetime import datetime

class Logger:
    @staticmethod
    def get_logger(log_config: LogConfig):

        # get logger
        logger = logging.getLogger("TTS_Logger")

        # format logging string
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        log_path = log_config.log_path.format(datetime.now().strftime('%d_%m_%Y-%H_%M'))

        # initiate file and console settings
        file_handler = logging.FileHandler(log_path)
        console_handler = logging.StreamHandler()

        # set format
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # set logging level
        logger.setLevel(log_config.log_level)

        # add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger