from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import os

# 🌍 Translate
def translate_text(text, dest_lang):
    try:
        translated = GoogleTranslator(source='auto', target=dest_lang).translate(text)
        return translated
    except:
        return "Translation failed"


# 🔊 Speak
def speak_in_language(text, lang="en"):
    try:
        filename = "voice.mp3"

        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

        pygame.mixer.quit()
        os.remove(filename)

    except Exception as e:
        print("Speech error:", e)