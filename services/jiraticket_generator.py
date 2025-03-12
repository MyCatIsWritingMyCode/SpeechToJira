import logging
from jira import JIRA
from models.app_config import *

class JiraGenerator:
    def __init__(self, logger : logging.Logger, config : Config):
        self.logger = logger
        self.config = config

    def login_and_authenticate(self):
        try:
            jira = JIRA(basic_auth=("email", "API token"))
        except Exception as e:
            self.logger.error(f"JIRA Log-In failed: {e}")
            raise

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