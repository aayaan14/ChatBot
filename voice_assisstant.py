import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()
engine.say("Let us Begin")
engine.runAndWait()

while 1:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening")
        audio = r.listen(source)
        text = r.recognize_google(audio)
        if 'stop' in text.lower():
            break
        print("Did you just say: ",text)
engine.say("That is the end. Thank you")
engine.runAndWait()

