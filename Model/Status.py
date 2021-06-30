class Status:
    number_of_pre_levels = 3

    young_man_strings = ['young man', 'young boy', 'young male']
    old_man_strings = ['old man', 'old male']
    young_woman_strings = ['young woman', 'young lady', 'young girl', 'young female']
    old_woman_strings = ['old woman', 'old lady', 'old female']

    def __init__(self, chat_id):
        self.chat_id = chat_id
        # can be male of female
        self.voice_gender = 'female'
        # can be young or old
        self.voice_age = 'old'
        self.pre_test = True
        self.level = 1
        self.number_of_questions = 0
        self.current_question = 0

    def has_not_agreed(self):
        return self.level == 1

    def has_not_set_number_of_questions(self):
        return self.level == 2

    def has_not_set_voice_properties(self):
        return self.level == 3

    def update_level(self):
        if self.level < Status.number_of_pre_levels:
            self.level += 1
        else:
            self.level += 1
            self.current_question += 1

    def reset_status(self):
        self.pre_test = True
        self.level = 1

    def get_current_question(self):
        return self.current_question

    @staticmethod
    def get_properties_of_voice(string):
        if string in Status.young_man_strings:
            return 'young', 'male'
        if string in Status.old_man_strings:
            return 'old', 'male'
        if string in Status.young_woman_strings:
            return 'young', 'female'
        if string in Status.old_woman_strings:
            return 'old', 'female'
        else:
            return None
