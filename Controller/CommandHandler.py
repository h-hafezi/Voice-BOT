import json
from urllib.request import urlopen

import main, Model.Status as Status
from Controller import Telegram
from Model.Chat import Chat as chat

URL = main.URL


def start(server):
    # Auxiliary variable for defining commands
    command = 'getme'
    response = urlopen(URL + command)
    line = json.loads(Telegram.decode_utf8(response))
    status = line['ok']

    command = 'getUpdates'

    # getting all updates before server was started running and delete them
    response = urlopen(URL + command)
    updates = json.loads(Telegram.decode_utf8(response))
    Telegram.delete_all_updates(updates)

    while status:

        command = 'getUpdates'

        # reading the url to get the current updates
        response = urlopen(URL + command)
        updates = json.loads(Telegram.decode_utf8(response))
        # Number of New Messages Received
        number_of_updates = len(updates['result'])

        # if updates are available to process
        if number_of_updates != 0:

            # reducing updates by one
            Telegram.reduce_updates(updates)

            # make the current message ready for processing
            message = updates['result'][0]['message']
            print(message)

            # read the chat id
            chat_id = str(message['chat']['id'])

            # the person is already known to bot
            if chat.is_there_chat_id(chat_id):
                known_user(chat_id, message, server)
            # the person is unknown to bot
            else:
                unknown_user(chat_id)

        print('server is waiting')


####################################################################################################################
#################################################### unknown user ##################################################
####################################################################################################################

def unknown_user(chat_id):
    print('0- here')
    chat(chat_id)
    string = 'سلام! به ربات ما خوش امدید، ما از شما تعدادی سوال می پرسیم و در نهایت به شما امتیاز داده میشود، هر موقع ' \
             'اماده بودید بگویید بله! '
    Telegram.send_voice(chat_id, string)


####################################################################################################################
#################################################### known user ####################################################
####################################################################################################################

def known_user(chat_id, message, server):
    ############################################### initializing ##################################################

    # get status of users and behave accordingly
    status = chat.get_status_with_chat_id(chat_id)
    number_of_questions = chat.get_number_of_questions(chat_id)
    final_status = number_of_questions + 2
    # in this case we're still waiting that they say بله

    ################################################################################################################
    ########################################### waiting to say yes #################################################
    ################################################################################################################

    if status.has_not_agreed() and 'voice' in message:
        print('1- here')
        text = Telegram.speech_to_text_from_file_id(message, server).lower()
        if text == 'yes':
            print('2- here')
            Telegram.send_voice(chat_id, 'عددی بین یک تا پنچ را با وویس به زبان انگلیسی بگویید')
            chat.update_status(chat_id)
            return
        else:
            Telegram.send_voice(chat_id, 'برای شروع لطفا بگویید بله')
    elif status.has_not_agreed():
        Telegram.send_voice(chat_id, 'برای شروع لطفا بگویید بله')

    ################################################################################################################
    ############################################## number of questions #############################################
    ################################################################################################################

    # status two, when we're waiting to get a voice containing a number in range [1, 5]
    if status.has_not_set_number_of_questions() and 'voice' in message:
        print('4- here')
        number = Telegram.speech_to_text_from_file_id(message, server)
        if number in list(map(str, range(1, 6))):
            chat.update_status(chat_id)
            chat.set_number_of_questions(chat_id, int(number))
            Telegram.send_voice(chat_id, 'لطفا جنسیت و سن من را تنظیم کنید')
            return
        else:
            Telegram.send_voice(chat_id, 'لطفا عددی در بازه بیان شده بگویید')
    elif status.has_not_set_number_of_questions() == 2:
        Telegram.send_voice(chat_id, 'لطفا عددی در بازه بیان شده بگویید')

    ################################################################################################################
    ############################################## voice properties ################################################
    ################################################################################################################

    # the test phase, after receiving wav file, we should evaluate it
    if status.has_not_set_voice_properties() and 'voice' in message:
        print('5- here')
        string = Telegram.speech_to_text_from_file_id(message, server)
        properties = Status.Status.get_properties_of_voice(string)
        if properties is not None:
            status.voice_age = properties[0]
            status.voice_gender = properties[1]
            Telegram.send_voice(chat_id, 'اطلاعات با موفقیت وارد شد')
            chat.update_status(chat_id)
            Telegram.send_question(chat_id)
            return
        else:
            Telegram.send_voice(chat_id, 'لطفا به صورت درست سن و جنسیت ربات را بگویید')
    elif status.has_not_set_voice_properties():
        Telegram.send_voice(chat_id, 'لطفا به صورت درست سن و جنسیت ربات را بگویید')

    ################################################################################################################
    ################################################# questions ####################################################
    ################################################################################################################

    if status.get_current_question() <= number_of_questions and status.get_current_question():
        print(f'{status.get_current_question()=}')
        if 'voice' in message:
            answer = Telegram.speech_to_text_from_file_id(message, server)
            # the case they give right answer
            if chat.is_answer_correct(chat_id, answer):
                chat.increase_score(chat_id)
                string = 'افرین! جواب شما صحیح است'
                Telegram.send_voice(chat_id, string)

            # if they had the wrong answer
            else:
                string = 'متاسفانه جواب شما غلط است'
                Telegram.send_voice(chat_id, string)
            if status.current_question < number_of_questions:
                print(f'{status=}')
                chat.update_status(chat_id)
                Telegram.send_question(chat_id)

    ################################################################################################################
    ################################################# the end ####################################################
    ################################################################################################################

    if status.get_current_question() == number_of_questions and number_of_questions:
        text = 'شما نمره' + str(chat.get_score(chat_id)) + ' کسب کردید و '
        text += 'آزمون شما تمام شد. در صورت که میخواهید دوباره شروع کنید، مجددا به انگلیسی بگویید بله!'
        Telegram.send_voice(chat_id, text)
        chat.get_chat_with_id(chat_id).status.reset_status()
        chat.get_chat_with_id(chat_id).score = 0
