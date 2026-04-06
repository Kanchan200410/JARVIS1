import pyttsx3

engine = pyttsx3.init('sapi5')
engine.say("If you hear this, audio is working")
engine.runAndWait()