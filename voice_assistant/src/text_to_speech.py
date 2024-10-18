import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    if 'fr' in voice.languages[0]:
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 170)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()