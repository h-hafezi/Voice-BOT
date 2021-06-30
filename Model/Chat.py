from Controller import Database
from Model.Status import Status


class Chat:
    all_chats = dict()

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.status = Status(chat_id)
        self.score = 0
        self.number_of_questions = 0
        Chat.all_chats[chat_id] = self

    ################################## chat methods ##################################

    @staticmethod
    def is_there_chat_id(chat_id):
        return chat_id in list(Chat.all_chats)

    ################################## score methods ##################################

    @staticmethod
    def get_score(chat_id):
        return Chat.get_chat_with_id(chat_id).score

    @staticmethod
    def reset_score(chat_id):
        Chat.get_chat_with_id(chat_id).score = 0

    @staticmethod
    def increase_score(chat_id):
        Chat.get_chat_with_id(chat_id).score += 1

    ################################# question methods #################################

    @staticmethod
    def set_number_of_questions(chat_id, number_of_questions):
        person = Chat.get_chat_with_id(chat_id)
        person.number_of_questions = number_of_questions
        person.questions = Database.get_random_list(number_of_questions)
        print(person.questions)

    @staticmethod
    def get_number_of_questions(chat_id):
        return Chat.get_chat_with_id(chat_id).number_of_questions

    @staticmethod
    def get_current_question(chat_id):
        person = Chat.get_chat_with_id(chat_id)
        return person.questions[person.status.current_question - 1]
        # return person.questions[person.status - 4]

    # a chat status can be the following:
    # 1- waiting for saying 'بله'
    # 2- waiting to say number of questions
    # 3- ...
    #
    # and finally when status is equal with "number of questions plus 3"
    # then status is reset to 1 again
    #
    # then the result is sent and they're said if
    # they want to start over say '/start' and then
    # their status will be one again

    @staticmethod
    def get_chat_with_id(chat_id):
        return Chat.all_chats[chat_id]

    @staticmethod
    def get_status_with_chat_id(chat_id):
        return Chat.all_chats[chat_id].status

    @staticmethod
    def update_status(chat_id):
        Chat.all_chats[chat_id].status.update_level()

    @staticmethod
    def reset_status(chat_id):
        Chat.all_chats[chat_id].status.reset_status()

    @staticmethod
    def is_answer_correct(chat_id, answer):
        question = Chat.get_current_question(chat_id)
        print(question)
        return Database.questions[question] == answer
