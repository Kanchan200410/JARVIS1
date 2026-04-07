import pyautogui
import webbrowser
import screen_brightness_control as sbc
import os
import time
import urllib.parse

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

# 📱 Send WhatsApp Message (BEST METHOD 🔥)
def send_whatsapp_web(phone_number, message):

    # Encode message for URL
    # Encode message
    msg = urllib.parse.quote(message)

    # Open WhatsApp chat
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={msg}"
    webbrowser.open(url)

    # Wait for full load
    time.sleep(15)   # ⬅️ increase time (VERY IMPORTANT)

    # Click center of screen to ensure focus
    pyautogui.click(800, 500)   # adjust if needed
    time.sleep(1)

    # Press enter
    pyautogui.press("enter")

    return "Message sent successfully"