import random

questions = dict()


def add(persian, english):
    questions[persian] = english


def get_random_list(number):
    persian_questions = list(questions.keys())
    random.shuffle(persian_questions)
    return persian_questions[:number]


def initialize_questions():
    add('حالت چطوره؟', 'how are you')
    add('مادرت چطوره؟', 'how is your mother')
    add('پدرت چطوره؟', 'how is your father')
    add('خواهرت چطوره؟', 'how is your sister')
    add('برادرت چطوره؟', 'how is your brother')
    add('والدینت چطورن؟', 'how are your parents')
    add('زنت چطوره؟', 'how is your wife')
    add('شوهرت چطوره؟', 'how is your husband')
    add('همسرت چطوره؟', 'how is your spouse')
    add('نامزدت چطوره؟', 'how is your fiance')
    add('بچت چطوره؟', 'how is your child')
    add('بچه هات چطورن؟', 'how are your children')
    add('پسرت چطوره؟', 'how is your son')
    add('دخترت چطوره؟', 'how is your daughter')
    add('مادربزرگ ت چطوره؟', 'how is your grandmother')
    add('پدربزرگت چطوره؟', 'how is your grandfather')
    add('نوه ات چطوره؟', 'how is your grandchild')
    add('نوه ات چطوره؟ (پسر)', 'how is your grandson')
