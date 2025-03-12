import json
from models.app_config import *

class ConfigLoader:
    def __init__(self, path : str):
        self.path = path

    def load(self) -> (AppConfig, LogConfig):
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
        except:
            error = "Could not load config file, please check the path"
            raise Exception(error)
        return AppConfig(**data["app_config"]), LogConfig(**data["logging"]), ModelConfig(**data["models"])