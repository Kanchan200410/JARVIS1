from ai_brain import ask_ai
from memory import remember, recall
from chat_memory import add_chat
from system_control import *
from contacts_db import add_contact, get_contact

import os
import webbrowser


def execute_command(command):

    command = command.lower().strip()

    # =========================
    # 🧠 MEMORY: NAME
    # =========================
    if "my name is" in command:
        name = command.split("my name is")[-1].strip()

        remember("name", name)

        add_chat("user", command)
        add_chat("assistant", f"Your name is {name}")

        return f"Okay, I will remember that your name is {name}"

    elif "name" in command and "my" in command:
        name = recall("name")
        return f"Your name is {name}" if name else "I don't know your name yet"

    # =========================
    # 🧠 MEMORY: GENERIC
    # =========================
    elif "remember that" in command:
        info = command.replace("remember that", "").strip()
        remember(info, True)
        return f"Okay, I will remember that {info}"

    elif "do you remember" in command:
        info = command.replace("do you remember", "").strip()
        value = recall(info)
        return f"Yes, I remember that {info}" if value else "No, I don't remember that"

    # =========================
    # 🧠 CUSTOM INFO
    # =========================
    elif "my" in command and "is" in command:
        parts = command.split("is")

        if len(parts) >= 2:
            key = parts[0].replace("my", "").strip()
            value = parts[1].strip()

            remember(key, value)
            return f"I will remember that your {key} is {value}"

    elif "what is my" in command:
        key = command.replace("what is my", "").strip()
        value = recall(key)
        return f"Your {key} is {value}" if value else f"I don't know your {key}"

    # =========================
    # 🔍 SEARCH
    # =========================
    elif "youtube search" in command:
        query = command.replace("youtube search", "").strip()

        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Searching YouTube for {query}"
        else:
            return "What do you want to search on YouTube?"

    elif "search" in command:
        query = command.replace("search", "").strip()

        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query}"
        else:
            return "What do you want to search?"

    # =========================
    # 📂 CREATE FOLDER
    # =========================
    elif "create" in command and "folder" in command:

        path = "."

        if "b drive" in command:
            path = "B:\\"
        elif "c drive" in command:
            path = "C:\\"
        elif "d drive" in command:
            path = "D:\\"

        name = command.split("name")[-1].strip() if "name" in command else "new_folder"
        full_path = os.path.join(path, name)

        try:
            os.makedirs(full_path, exist_ok=True)
            return f"Folder {name} created in {path}"
        except:
            return "Failed to create folder"

    # =========================
    # 📄 CREATE FILE
    # =========================
    elif "create file" in command:
        name = command.replace("create file", "").strip()

        try:
            with open(name, "w") as f:
                f.write("")
            return f"File {name} created"
        except:
            return "Failed to create file"

    # =========================
    # 🗑️ DELETE FILE
    # =========================
    elif "delete file" in command:
        filename = command.replace("delete file", "").strip()

        import os
        import string

        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

        for drive in drives:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    if filename.lower() in file.lower():
                        full_path = os.path.join(root, file)

                        try:
                            os.remove(full_path)
                            return f"Deleted {file} from {root}"
                        except:
                            return "Permission denied"

        return "File not found"

    # =========================
    # 📂 OPEN FOLDER
    # =========================
    elif "open folder" in command:
        path = command.replace("open folder", "").strip()

        try:
            os.startfile(path)
            return f"Opening folder {path}"
        except:
            return "Folder not found"

    # =========================
    # 🌐 WEB
    # =========================
    elif "open website" in command:
        site = command.replace("open website", "").strip()
        webbrowser.open(f"https://{site}")
        return f"Opening {site}"

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    elif "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    elif "open anime" in command:
        webbrowser.open("https://aniwatch.re/")
        return "opening anime"

    # =========================
    # 💻 SOFTWARE
    # =========================
    elif "open notepad" in command:
        os.system("start notepad")
        return "Opening Notepad"

    elif "open chrome" in command:
        os.system("start chrome")
        return "Opening Chrome"

    elif "open vscode" in command:
        os.system("code")
        return "Opening VS Code"

    # =========================
    # 🔊 VOLUME
    # =========================
    elif "volume up" in command:
        return volume_up()

    elif "volume down" in command:
        return volume_down()

    # =========================
    # 💡 BRIGHTNESS
    # =========================
    elif "brightness up" in command:
        return brightness_up()

    elif "brightness down" in command:
        return brightness_down()

    # =========================
    # 📝 WRITE NOTE
    # =========================
    elif "write note" in command:
        text = command.replace("write note", "").strip()
        return write_note(text if text else "This is a note from Jarvis")

    # =========================
    # ⌨️ TYPE
    # =========================
    elif "type" in command:
        text = command.replace("type", "").strip()

        if text:
            os.system("start notepad")
            import time
            time.sleep(2.5)
            return type_text(text)
        else:
            return "What should I type?"

    # =========================
    # ⏰ TIME / DATE
    # =========================
    elif "time" in command:
        import datetime
        return datetime.datetime.now().strftime("Time is %I:%M %p")

    elif "date" in command:
        import datetime
        return datetime.datetime.now().strftime("Today is %d %B %Y")

    #SAVE CONTACTS

    elif "save contact" in command:
        parts = command.replace("save contact", "").strip().split()

        if len(parts) >= 2:
            name = parts[0]
            number = parts[1]

            return add_contact(name, number)

        return "Give name and number"

    #SEND WHATSAPP

    elif "send whatsapp" in command:
        parts = command.replace("send whatsapp", "").strip()

        if parts:
            data = parts.split(" ", 1)

            name = data[0]
            message = data[1] if len(data) > 1 else "Hello"

            number = get_contact(name)

            if number:
                return send_whatsapp_web(number, message)
            else:
                return f"Contact {name} not found"


    # =========================
    # ❌ EXIT
    # =========================
    elif "exit" in command or "stop" in command:
        return False

    # =========================
    # 🤖 FALLBACK
    # =========================
    else:
        return None