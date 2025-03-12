import logging, re
from utilities.configuration_loader import ConfigLoader
from utilities.logger_utility import Logger
# from orchestrator import Orchestrator
# from services.speechtotext import SpeechToText
from services.topic_segmentator import NLPProcessor
# from services.jiraticket_generator import JiraGenerator
from utilities.configuration_loader import AppConfig, LogConfig, ModelConfig, Config

def main():
    logger : logging.Logger
    try:
        # Load configuration
        config_loader = ConfigLoader("resources/appsettings.json")
        app_config: AppConfig
        log_config: LogConfig
        model_config: ModelConfig
        (app_config, log_config, model_config) = config_loader.load()

        logger = Logger.get_logger(log_config)
        logger.info("Starting application...")

        config = Config(app_config, log_config, model_config)

        #tts_service = SpeechToText(logger, config)
        #tts_text = tts_service.transcribe("resources/audio_files/philosopher_lecture.mp3")
        #print(tts_text)
        data : str = ""
        with open('resources/lecture.txt', 'r') as file:
            data = file.read().replace('\n', '')
        print(data)
        print('')

        #print(sentences)

        topic_processor = NLPProcessor(logger, config)
        segmented_text : list[str] = topic_processor.extract_topics(data)

        # jira_model_name = config.get("jira_generator")["model_name"]
        # jira_generator = JiraGenerator(jira_model_name, logger)
        #
        # # Orchestrator
        # orchestrator = Orchestrator(stt_service, topic_processor, jira_generator, logger)

        # Run the tool
        # audio_file = "path/to/audio.mp3"
        # orchestrator.run(audio_file)

    except Exception as e:
        raise Exception(f"Application encountered an error: {e}")


if __name__ == "__main__":
    main()