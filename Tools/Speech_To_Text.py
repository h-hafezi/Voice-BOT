import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def speech_to_text():
    try:
        # use the microphone as source for input.
        harvard = sr.AudioFile('voice.wav')
        with harvard as source:
            audio = r.record(source)
            # adjust the energy threshold based on
            # the surrounding noise level
            text = r.recognize_google(audio)
            return text.lower()
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ''
    except sr.UnknownValueError:
        print("unknown error occured")
        return ''
