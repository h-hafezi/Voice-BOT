from urllib.request import urlopen
from urllib.parse import quote

URL = 'http://api.farsireader.com/ArianaCloudService/ReadTextGET'
KEY = 'J3PDY9ETTJSHJSC'


def text_to_speech(text, gender='female', pitch=0):
    if gender.lower() == 'female':
        gender = 'Female1'
    else:
        gender = 'Male1'
    response = urlopen(URL + f'?APIKey={KEY}&Text={quote(text)}&Speaker={gender}&Format=ogg&PitchLevel={pitch}', timeout=120)
    with open('persian.ogg', 'wb') as f:
        f.write(response.read())


