import tkinter as tk
from threading import Thread
import math
import random
import time

# ✅ EXISTING IMPORTS
from voice import listen, speak
from my_commands import execute_command
from ai_brain import ask_ai

# 🔥 NEW IMPORTS (VISION)
from vision import capture_screen, capture_camera, process_vision
from ai_brain import explain_vision


# =========================
# COLORS
# =========================
BG_DARK      = "#070d14"
BG_PANEL     = "#050b12"
BG_CARD      = "#0a1a24"
BORDER_DIM   = "#0d2a3a"
BORDER_MID   = "#1a5c7a"
BORDER_BRIGHT= "#1a7a9a"
CYAN         = "#00d4ff"
CYAN_DIM     = "#1a7a9a"
CYAN_FAINT   = "#1a5c7a"
PURPLE       = "#8040ff"
PURPLE_DIM   = "#2a0d5a"
RED_ALERT    = "#ff4060"
GREEN_OK     = "#00ff88"
AMBER        = "#ffaa00"
TEXT_CYAN    = "#7ad4f0"
TEXT_PURPLE  = "#b88aff"


class JarvisApp:
    def __init__(self):
        self.running = True
        self.status  = "IDLE"
        self.start_time = time.time()

        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.geometry("900x550")
        self.root.configure(bg=BG_DARK)

        self._build_ui()
        Thread(target=self._voice_loop, daemon=True).start()

        self._greet()
        self.root.mainloop()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        self.chat_box = tk.Text(
            self.root,
            bg=BG_DARK,
            fg=TEXT_CYAN,
            font=("Courier New", 12),
            wrap="word"
        )
        self.chat_box.pack(fill="both", expand=True)

        self.entry = tk.Entry(
            self.root,
            bg=BG_PANEL,
            fg=CYAN,
            font=("Courier New", 12)
        )
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", lambda e: self._send())

    # =========================
    # CHAT
    # =========================
    def _chat(self, text):
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.see(tk.END)

    # =========================
    # STATUS
    # =========================
    def _set_status(self, status):
        self.status = status
        print("STATUS:", status)

    # =========================
    # COMMAND PROCESSOR (UPDATED)
    # =========================
    def _process_command(self, command):
        if not command:
            return

        self._chat("You: " + command)
        self._set_status("THINKING")

        def run():
            result = execute_command(command)

            # =========================
            # 👁️ VISION HANDLER
            # =========================
            if result is None:

                if "screen" in command:
                    self._chat("Jarvis: Analyzing screen...")
                    frame = capture_screen()

                    if frame is not None:
                        data = process_vision(frame)
                        response = explain_vision(data)
                    else:
                        response = "Failed to capture screen"

                elif "camera" in command:
                    self._chat("Jarvis: Opening camera...")
                    frame = capture_camera()

                    if frame is not None:
                        data = process_vision(frame)
                        response = explain_vision(data)
                    else:
                        response = "Camera not working"

                else:
                    response = ask_ai(command)

            else:
                if result is False:
                    speak("Goodbye")
                    self.running = False
                    self.root.destroy()
                    return

                response = result

            # =========================
            # OUTPUT
            # =========================
            self._set_status("SPEAKING")
            self._chat("Jarvis: " + response)

            speak(response)

            self._set_status("IDLE")

        Thread(target=run, daemon=True).start()

    def _send(self):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        self._process_command(cmd)

    # =========================
    # VOICE LOOP
    # =========================
    def _voice_loop(self):
        while self.running:
            self._set_status("LISTENING")
            command = listen()

            if command:
                self._process_command(command)

            self._set_status("IDLE")
            time.sleep(0.1)

    # =========================
    # GREETING
    # =========================
    def _greet(self):
        msg = "Hello, I am Jarvis. How can I help you?"
        self._chat("Jarvis: " + msg)
        speak(msg)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    JarvisApp()