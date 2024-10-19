import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    if hasattr(voice, 'languages') and len(voice.languages) > 0 and 'fr' in voice.languages[0]:
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 170)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

