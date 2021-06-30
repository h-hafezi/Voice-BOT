from Controller import Database, CommandHandler


class server:

    def __init__(self, token):
        self.chat_ids = {}
        self.token = token

    def start(self):
        Database.initialize_questions()
        CommandHandler.start(self)
