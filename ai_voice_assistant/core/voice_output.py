import pyttsx3

engine = None
tts_initialized_successfully = False

def initialize_tts():
    """Initializes the text-to-speech engine."""
    global engine, tts_initialized_successfully
    try:
        engine = pyttsx3.init()
        if engine:
            # Check if voices are available as a simple test
            voices = engine.getProperty('voices')
            if voices:
                tts_initialized_successfully = True
                print("TTS engine initialized successfully.")
            else:
                print("TTS engine initialized, but no voices found. TTS may not work.")
                engine = None # Treat as failure
                tts_initialized_successfully = False
        else:
            print("Failed to initialize pyttsx3 engine instance.")
            tts_initialized_successfully = False

    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        print("Text-to-speech will not be available. Falling back to text output.")
        engine = None
        tts_initialized_successfully = False

def is_tts_available() -> bool:
    """Checks if the TTS engine was initialized successfully."""
    return tts_initialized_successfully

def speak(text: str):
    """Converts text to speech and speaks it.
    Falls back to printing if TTS engine is not available."""
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error during TTS speech: {e}")
            print(f"Assistant (fallback): {text}") # Fallback to print
    else:
        print(f"Assistant (TTS disabled): {text}")

# Initialize TTS when the module is loaded
initialize_tts()

if __name__ == '__main__':
    # Test the speak function
    print("Testing TTS...")
    speak("Hello, this is a test of the text to speech system.")
    speak("If you can hear this, the TTS is working.")
    # Test fallback
    engine = None
    speak("This message should be printed as a fallback.")
