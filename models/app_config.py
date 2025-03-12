from dataclasses import dataclass

@dataclass
class AppConfig:
    file_path: str

@dataclass
class LogConfig:
    log_path: str
    log_level: str

@dataclass
class ModelConfig:
    tts_model: str
    topic_seg: str
    jira_gen: str
    jira_email: str
    jira_api_token: str

@dataclass
class Config:
    app_config: AppConfig
    log_config: LogConfig
    model_config: ModelConfig