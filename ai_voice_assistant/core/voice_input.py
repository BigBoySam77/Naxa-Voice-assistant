import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

def listen_for_audio(timeout: int = 5, phrase_time_limit: int = 10) -> str | None:
    """
    Listens for audio input from the microphone and tries to recognize it.

    Args:
        timeout: Time in seconds to wait for a phrase to start.
        phrase_time_limit: Maximum time in seconds a phrase can be.

    Returns:
        The recognized text as a string, or None if recognition fails or an error occurs.
    """
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise to improve recognition
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Adjusted for ambient noise. Say something!")
            # Listen for the first phrase and extract it into audio data
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return None
        except Exception as e:
            print(f"Could not access microphone or listen: {e}")
            return None

    try:
        print("Recognizing...")
        # Recognize speech using Google Web Speech API (default)
        # This requires an internet connection.
        # For offline recognition, other engines like Sphinx can be used but require setup.
        text = r.recognize_google(audio)
        print(f"User said: {text}")
        return text.lower() # Convert to lowercase for easier processing
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during speech recognition: {e}")
        return None

if __name__ == '__main__':
    print("Testing voice input. Please say something into your microphone.")
    # Note: This test might not work in all sandbox environments due to microphone access.
    # It's primarily for local testing by the user.

    # Attempt to get input twice
    for i in range(2):
        print(f"\nAttempt {i+1}:")
        recognized_text = listen_for_audio(timeout=5, phrase_time_limit=5)
        if recognized_text:
            print(f"Recognized: '{recognized_text}'")
        else:
            print("No text recognized or an error occurred.")

        if i == 0 and not recognized_text:
            print("If no audio was captured, please ensure your microphone is connected and configured.")
            print("This test will try one more time.")

    print("\nVoice input test finished.")
