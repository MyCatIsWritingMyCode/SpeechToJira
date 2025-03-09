class Orchestrator:
    def __init__(self, stt_service, topic_processor, jira_generator, logger):
        self.stt_service = stt_service
        self.topic_processor = topic_processor
        self.jira_generator = jira_generator
        self.logger = logger

    def run(self, audio_file):
        try:
            self.logger.info("Starting workflow...")
            text = self.stt_service.transcribe(audio_file)
            topics = self.topic_processor.extract_topics(text)
            jira_tickets = self.jira_generator.generate_tickets(topics)
            self.logger.info(f"Generated {len(jira_tickets)} JIRA tickets.")
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            raise