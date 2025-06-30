# ai_voice_assistant/core/intent_handler.py
import json

def load_knowledge_base_from_path(file_path: str) -> dict:
    """Loads the knowledge base from a JSON file path."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Knowledge base file not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return {}

def recognize_intent(text: str, knowledge_base: dict) -> tuple[str | None, str | None]:
    """
    Recognizes intent from user text based on keywords in the knowledge base.

    Args:
        text: The user's spoken input, converted to lowercase text.
        knowledge_base: The loaded knowledge base dictionary.

    Returns:
        A tuple containing:
        - intent_key (str | None): The key of the recognized intent (e.g., "check_order_status") or None.
        - response (str | None): The predefined response for that intent or None.
    """
    if not text:
        return None, None

    intents_data = knowledge_base.get("intents", {})
    fallback_response = knowledge_base.get("fallback", {}).get("default", "I'm sorry, I didn't understand that.")

    for intent_key, intent_info in intents_data.items():
        keywords = intent_info.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in text.lower(): # Ensure keyword matching is case-insensitive
                return intent_key, intent_info.get("response", fallback_response)

    return None, fallback_response # If no intent is matched, return None for intent and the fallback response

if __name__ == '__main__':
    # Example Usage (requires knowledge_base.json to be in ../data/ relative to this file for direct run)
    # This assumes you run this file directly from the 'core' directory.
    # For robust testing, it's better to test through main.py or a dedicated test suite.

    # Construct path to knowledge base for testing
    import os
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    KB_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "data", "knowledge_base.json")

    test_kb = load_knowledge_base_from_path(KB_PATH)

    if not test_kb:
        print("Could not load knowledge base for testing intent handler.")
    else:
        print("Knowledge base loaded for testing intent handler.")
        queries = [
            "I want to check my order status",
            "Tell me about your products",
            "I need to talk to support",
            "What's the weather like?", # Should trigger fallback
            "track my package" # Should trigger order status
        ]

        for query in queries:
            intent, response = recognize_intent(query, test_kb)
            print(f"\nQuery: '{query}'")
            if intent:
                print(f"  Intent: {intent}")
                print(f"  Response: {response}")
            else:
                print(f"  Intent: Not recognized")
                print(f"  Response: {response}")
