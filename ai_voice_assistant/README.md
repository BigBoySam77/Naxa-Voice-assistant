# AI Voice Assistant

This project is an AI-powered voice assistant designed to help businesses handle customer calls.

## Setup

1.  Clone the repository.
2.  It is highly recommended to use a Python virtual environment for local development:
    \`\`\`bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use \`venv\\Scripts\\activate\`
    \`\`\`
3.  Install the dependencies:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`
    *Note: The `requirements.txt` is generated based on the sandbox environment. You might need to adjust it based on your specific OS for libraries like `pyttsx3` which can have system dependencies (e.g., espeak on Linux), or for `PyAudio` if `SpeechRecognition` requires it for microphone access (often needed on Linux/macOS).*

## Running the Assistant

To run the assistant, navigate to the project's root directory and execute:
\`\`\`bash
python ai_voice_assistant/main.py
\`\`\`
If you encounter issues with file paths, ensure you are running the script from the directory containing the \`ai_voice_assistant\` folder.

## How it Works
The assistant listens for voice input via your microphone, processes it to understand intent, and responds using text-to-speech. Key interactions and responses are defined in `ai_voice_assistant/data/knowledge_base.json`, allowing for customization of business-specific queries.

## Customization
To tailor the assistant's responses and recognized intents:
- Modify `ai_voice_assistant/data/knowledge_base.json`.
- Add new intents with associated keywords and responses.
- Adjust greetings, farewells, and fallback messages.

## Project Structure
- \`ai_voice_assistant/main.py\`: Main script to run the assistant.
- \`ai_voice_assistant/core/\`: Core logic for voice input, output, and intent handling.
- \`ai_voice_assistant/utils/\`: Utility functions.
- \`ai_voice_assistant/data/\`: Data files like the knowledge base.
- \`ai_voice_assistant/requirements.txt\`: Python dependencies.
- \`README.md\`: This file.
- \`.gitignore\`: Specifies intentionally untracked files that Git should ignore.

## Future Considerations
This initial version provides a basic framework. Future enhancements could include:
- **Telephony Integration:** Connecting to actual phone lines (e.g., using Twilio).
- **Advanced NLU:** Using sophisticated Natural Language Understanding engines (e.g., Rasa, spaCy, cloud AI services) for better intent recognition and entity extraction.
- **Database Integration:** Storing and retrieving customer data, order information, etc.
- **CRM Integration:** Logging calls and customer interactions in CRM systems.
- **Contextual Conversations:** Enabling multi-turn dialogues where the assistant remembers context.
- **Sentiment Analysis:** Detecting customer sentiment to adapt responses or escalate.
- **Scalability & Deployment:** Preparing for handling multiple calls and deploying to servers/cloud.
- **Enhanced STT/TTS:** Integrating with more advanced speech services or offline engines.
- **Automated Testing:** Building a comprehensive test suite.
- **Logging & Monitoring:** Implementing robust logging for diagnostics and performance.
