from langchain.agents import Tool
from utils.email_sender import EmailSender


class StableMessage(Tool):
    email_sender: EmailSender = None
    email_config: dict = None

    def sender_email(self):
        if not self.email_config:
            return
        receiver = self.email_config["receiver"]
        subject = self.email_config["subject"]
        content = self.email_config["content"]
        self.email_sender.send_email(receiver, subject, content)

    def __init__(self, config):
        def func(input) -> str:
            self.sender_email()
            return config["rules"]["message"]

        situation = config["situation"]

        description = f"useful for when {situation}."

        super().__init__(
            name=f"weather_search",
            func=func,
            description=description,
            return_direct=True,
        )

        self.email_sender = EmailSender()
        if "email" in config["rules"]:
            self.email_config = config["rules"]["email"]
