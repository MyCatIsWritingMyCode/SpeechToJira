class DeepSeekJiraGenerator:
    def __init__(self, model_name, logger):
        self.logger = logger
        self.logger.info(f"Initialized JIRA generator model: {model_name}")

    def generate_tickets(self, topics):
        try:
            tickets = []
            for topic in topics:
                ticket_type = self._determine_ticket_type(topic)
                tickets.append({
                    "title": topic["title"],
                    "description": topic["content"],
                    "type": ticket_type
                })
            return tickets
        except Exception as e:
            self.logger.error(f"JIRA ticket generation failed: {e}")
            raise

    def _determine_ticket_type(self, topic):
        if "error" in topic["content"].lower() or "bug" in topic["content"].lower():
            return "bug"
        elif "feature" in topic["content"].lower():
            return "story"
        return "epic"