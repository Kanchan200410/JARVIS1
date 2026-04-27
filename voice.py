import asyncio
import edge_tts
import pygame
import threading
import speech_recognition as sr
import time
import os

is_playing = False

# =========================
# 🔊 PLAY AUDIO (AUTO DELETE)
# =========================
def play_audio(file):
    global is_playing

    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    is_playing = True

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    is_playing = False

    # ✅ VERY IMPORTANT (release file)
    try:
        pygame.mixer.music.unload()
    except:
        pass

    # ✅ DELETE FILE AFTER PLAY
    try:
        os.remove(file)
    except:
        pass


# =========================
# 🔊 SPEAK FUNCTION
# =========================
def speak(text):
    short_text = text[:200]
    print("Jarvis:", text)

    threading.Thread(
        target=lambda: asyncio.run(generate_and_play(short_text))
    ).start()


# =========================
# 🔊 GENERATE + PLAY
# =========================
async def generate_and_play(text):
    import uuid
    file = f"voice_{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
    await communicate.save(file)

    play_audio(file)   # file gets deleted after playing


# =========================
# 🎤 LISTEN (NO INTERRUPT)
# =========================
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except:
        return ""