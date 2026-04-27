from voice import speak, listen
from my_commands import execute_command
from ai_brain import ask_ai, explain_vision

# 🔥 NEW IMPORT (vision module)
from vision import capture_screen, capture_camera, process_vision


def run_jarvis():
    speak("Hey! Jarvis here.")

    while True:
        command = listen()

        if command:
            print("COMMAND:", command)

            result = execute_command(command)

            print("RESULT:", result)

            # =========================
            # 👁️ VISION HANDLER (NEW)
            # =========================
            if result is None:

                # 🖥️ Screen
                if "screen" in command:
                    speak("Analyzing your screen")

                    frame = capture_screen()

                    if frame is not None:
                        data = process_vision(frame)
                        response = explain_vision(data)
                        speak(response)
                    else:
                        speak("Failed to capture screen")

                    continue

                # 🎥 Camera
                elif "camera" in command:
                    speak("Opening camera")

                    frame = capture_camera()

                    if frame is not None:
                        data = process_vision(frame)
                        response = explain_vision(data)
                        speak(response)
                    else:
                        speak("Camera not working")

                    continue

            # =========================
            # ORIGINAL LOGIC (UNCHANGED)
            # =========================
            if result is False:
                speak("Goodbye!")
                break

            elif isinstance(result, str):
                speak(result)

            else:
                # 🤖 AI fallback
                response = ask_ai(command)
                speak(response)


if __name__ == "__main__":
    run_jarvis()