import pyautogui
import screen_brightness_control as sbc
import os
import time

pyautogui.FAILSAFE = False


# 🔊 Volume
def volume_up():
    pyautogui.press("volumeup")
    return "Volume increased"


def volume_down():
    pyautogui.press("volumedown")
    return "Volume decreased"


# 💡 Brightness
def brightness_up():
    sbc.set_brightness(100)
    return "Brightness increased"


def brightness_down():
    sbc.set_brightness(30)
    return "Brightness decreased"


# 📝 Write note (FIXED)
def write_note(text):
    os.system("start notepad")
    time.sleep(2.5)  # wait for notepad

    pyautogui.click()
    pyautogui.write(text, interval=0.05)

    return "Note written"


# ⌨️ Type anywhere (FIXED)
def type_text(text):
    time.sleep(1.5)
    pyautogui.write(text, interval=0.05)
    return "Typing completed"

import pyautogui
import webbrowser


import webbrowser
import pyautogui
import time


def open_whatsapp_web():
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(12)
    return "WhatsApp Web opened"


def send_whatsapp_web(contact_name, message):

    # Open WhatsApp Web
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(12)  # wait for full load

    # Focus search (better than clicking)
    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)

    # Type contact name
    pyautogui.write(contact_name, interval=0.05)
    time.sleep(2)

    pyautogui.press("enter")
    time.sleep(2)

    # Type message
    pyautogui.write(message, interval=0.05)
    time.sleep(1)

    pyautogui.press("enter")

    return f"Message sent to {contact_name}"