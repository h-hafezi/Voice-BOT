import json, requests
from urllib.request import urlopen
from urllib.parse import quote

import main
from Model import Chat
from Tools import Text_To_Speech, Speech_To_Text
import Convert
from Model.Chat import Chat as chat

URL = main.URL


def speech_to_text_from_file_id(message, server):
    file_id = message['voice']['file_id']
    response = json.loads(decode_utf8(urlopen(URL + 'getFile?file_id={}'.format(file_id))))
    file_path = response['result']['file_path']
    url = 'https://api.telegram.org/file/bot{}/{}'.format(server.token, file_path)
    r = requests.get(url, allow_redirects=True)
    open('voice.ogg', 'wb').write(r.content)
    Convert.convert('voice.ogg', 'voice.wav')
    answer = Speech_To_Text.speech_to_text()
    print(answer)
    return answer


def send_message(chat_id, text):
    command = 'sendMessage'
    text = quote(text.encode('utf-8'))
    msg = json.loads(decode_utf8(urlopen(URL + command + '?chat_id={}&text={}'.format(chat_id, text))))
    if not msg['ok']:
        raise ConnectionError(' message did not send properly')


def send_question(chat_id):
    question = chat.get_current_question(chat_id)
    send_voice(chat_id, 'لطفا عبارت زیر وُیس گرفته به انگلیسی بفرستید:' + '\n' + question)


def decode_utf8(string):
    decoded = ''
    for line in string:
        decoded += line.decode('utf-8')
    return decoded


def delete_all_updates(updates):
    try:
        for _ in range(len(updates['result'])):
            reduce_updates(updates)
    except Exception as e:
        print(e)


# reduce one of updates to not get recurring answers
def reduce_updates(updates):
    update_id = updates['result'][0]['update_id']
    command = 'getUpdates'
    # Giving the offset Telegram forgets all those messages before this update id
    return urlopen(URL + command + '?offset={}'.format(update_id + 1))


def send_voice(chat_id, text):
    status = chat.get_chat_with_id(chat_id).status
    pitch = 0 if status.voice_age == 'old' else 9
    Text_To_Speech.text_to_speech(text, status.voice_gender, pitch)
    files = {'voice': open('persian.ogg', 'rb')}
    status = requests.post(URL + 'sendVoice?chat_id={}'.format(chat_id), files=files)
    print(status)
