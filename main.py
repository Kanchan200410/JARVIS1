from voice import speak, listen
from my_commands import execute_command

def run_jarvis():
    speak("Hey! Jarvis here.")

    while True:
        command = listen()

        if command:
            print("COMMAND:", command)

            result = execute_command(command)

            print("RESULT:", result)   # 👈 ADD HERE

            if result is False:
                speak("Goodbye!")
                break

            elif isinstance(result, str):
                speak(result)

if __name__ == "__main__":
    run_jarvis()