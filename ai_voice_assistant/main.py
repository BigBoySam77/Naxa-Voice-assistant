# ai_voice_assistant/main.py
import json
import os
import sys
import time

# Get the directory where main.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Assume the project root is one level up from the SCRIPT_DIR
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Add project root and script directory to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Now we can import from core
from core import speak, listen_for_audio, initialize_tts, is_tts_available, recognize_intent

KNOWLEDGE_BASE_FILENAME = "knowledge_base.json"
KNOWLEDGE_BASE_PATH = os.path.join(SCRIPT_DIR, "data", KNOWLEDGE_BASE_FILENAME)

def load_knowledge_base(file_path: str) -> dict:
    """Loads the knowledge base from the JSON file."""
    if not os.path.exists(file_path):
        print(f"Error: Knowledge base file not found at {file_path}")
        alt_path = os.path.join(os.getcwd(), "ai_voice_assistant", "data", KNOWLEDGE_BASE_FILENAME)
        if os.path.exists(alt_path):
            print(f"Found at alternative path: {alt_path}")
            file_path = alt_path
        else:
            print(f"Also not found at {alt_path} (current dir: {os.getcwd()})")
            return {}

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: FileNotFoundError for {file_path} (inside try block)")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while loading knowledge base: {e}")
        return {}

def main_conversation_loop(knowledge_base: dict):
    """Handles the main conversation flow with the user."""

    fallback_response = knowledge_base.get("fallback", {}).get("default", "I'm sorry, I didn't quite catch that. Could you please say it again?")
    max_failed_attempts = 3
    failed_attempts = 0

    speak("Connecting you to the assistant.")
    time.sleep(0.5)

    greeting = knowledge_base.get("greetings", {}).get("default", "Hello! How can I help you today?")
    speak(greeting)

    active_call = True
    interaction_count = 0
    max_interactions = 5

    while active_call and interaction_count < max_interactions:
        interaction_count += 1
        print(f"\nInteraction {interaction_count}...")

        user_input = listen_for_audio(timeout=7, phrase_time_limit=10)

        if user_input:
            failed_attempts = 0
            print(f"User said: {user_input}")

            if any(exit_phrase in user_input for exit_phrase in ["goodbye", "bye", "exit", "quit", "nothing else", "that's it"]):
                speak(knowledge_base.get("farewells", {}).get("default", "Goodbye!"))
                active_call = False
                continue

            intent_key, response_from_intent = recognize_intent(user_input, knowledge_base)

            if intent_key:
                speak(response_from_intent)
                # If the intent isn't one that naturally leads to more questions from the assistant side
                # (e.g. "provide order number", "which product"), then ask if user needs more help.
                if intent_key not in ["check_order_status", "product_inquiry", "contact_support"]: # Add more as needed
                    time.sleep(0.5)
                    speak("Is there anything else I can help you with today?")
                    follow_up_input = listen_for_audio(timeout=5, phrase_time_limit=5)
                    if follow_up_input and any(neg_resp in follow_up_input for neg_resp in ["no", "nope", "nothing", "that's all"]):
                        speak(knowledge_base.get("farewells", {}).get("default", "Alright. Goodbye!"))
                        active_call = False
            else: # No specific intent recognized, use the fallback from recognize_intent (which is kb fallback)
                speak(response_from_intent) # This will be the fallback response

        else: # No valid input from listen_for_audio
            failed_attempts += 1
            if failed_attempts >= max_failed_attempts:
                speak("I'm having trouble understanding you. Let's end the call for now. Please try again later.")
                active_call = False
            else:
                speak(fallback_response) # General fallback if listening failed

        if not active_call:
            break

    if interaction_count >= max_interactions and active_call:
        speak("We've reached the maximum interaction limit for this session. " + knowledge_base.get("farewells", {}).get("default", "Goodbye!"))

    print("Conversation loop ended.")


def main():
    initialize_tts()
    if not is_tts_available():
        print("INFO: Text-to-Speech engine could not be initialized. Assistant will use text output only.")

    speak("System starting up.") # This will print if TTS is unavailable, or speak if available.

    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)

    if not knowledge_base:
        message = "Critical error: Failed to load essential knowledge base. The assistant cannot start."
        print(message)
        speak(message)
        return

    try:
        main_conversation_loop(knowledge_base)
    except Exception as e:
        print(f"An unexpected error occurred in the main loop: {e}")
        speak("I've encountered an unexpected problem and need to end the call. Please try again later.")
    finally:
        speak("AI Voice Assistant shutting down. Thank you.")
        print("AI Voice Assistant shut down.")

if __name__ == "__main__":
    main()
