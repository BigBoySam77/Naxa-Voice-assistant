# ai_voice_assistant/core/__init__.py

"""
Core package for the AI Voice Assistant.

This package contains the main functionalities:
- voice_input: For capturing and recognizing speech.
- voice_output: For synthesizing and speaking text.
- intent_handler: For understanding user intent (to be developed further).
"""

from .voice_input import listen_for_audio
from .voice_output import speak, initialize_tts, is_tts_available
from .intent_handler import recognize_intent

__all__ = [
    "listen_for_audio",
    "speak",
    "initialize_tts",
    "is_tts_available",
    "recognize_intent"
]
