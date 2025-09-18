import win32com.client as win  # Import the win32com library for Windows COM support

def greet_on_startup():
    # Create a speaker object using Windows Speech API
    speaker = win.Dispatch("SAPI.SpVoice")
    # Set the greeting message
    greeting = "Hello, Zeel!"
    # Speak the greeting aloud
    speaker.Speak(greeting)

if __name__ == "__main__":
    # Run the greet_on_startup function when the script is executed
    greet_on_startup()