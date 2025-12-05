#!/usr/bin/env python3
"""
Talk-to-Type: A speech-to-text tool that types what you speak.

This tool captures audio from your microphone, converts speech to text
using Google's Speech Recognition API, and automatically types the
recognized text.
"""

import sys
import threading
import time

try:
    import speech_recognition as sr
    from pynput.keyboard import Controller
except ImportError as e:
    print(f"Error: Missing required dependency - {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


class TalkToType:
    """Main class for the Talk-to-Type application."""

    # Default configuration values
    DEFAULT_LISTEN_TIMEOUT = 5  # seconds to wait for speech
    DEFAULT_PHRASE_TIME_LIMIT = 10  # max seconds for a phrase
    DEFAULT_ENERGY_THRESHOLD = 300

    def __init__(
        self,
        listen_timeout=None,
        phrase_time_limit=None,
        energy_threshold=None,
    ):
        """Initialize the speech recognizer and keyboard controller.

        Args:
            listen_timeout: Seconds to wait for speech before timeout (default: 5).
            phrase_time_limit: Max seconds for a single phrase (default: 10).
            energy_threshold: Microphone sensitivity threshold (default: 300).
        """
        self.recognizer = sr.Recognizer()
        self.keyboard = Controller()
        self.is_running = False
        self.listen_thread = None

        # Configuration
        self.listen_timeout = listen_timeout or self.DEFAULT_LISTEN_TIMEOUT
        self.phrase_time_limit = phrase_time_limit or self.DEFAULT_PHRASE_TIME_LIMIT

        # Adjust for ambient noise sensitivity
        self.recognizer.energy_threshold = (
            energy_threshold or self.DEFAULT_ENERGY_THRESHOLD
        )
        self.recognizer.dynamic_energy_threshold = True

    def type_text(self, text):
        """Type the given text using the keyboard controller.

        Args:
            text: The text string to type.
        """
        if text:
            self.keyboard.type(text)
            # Add a space after each phrase for natural typing,
            # but only if the text doesn't already end with whitespace
            if not text.endswith((" ", "\t", "\n")):
                self.keyboard.type(" ")

    def listen_and_type(self):
        """Continuously listen for speech and type recognized text."""
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready! Start speaking...")
            print("Press Ctrl+C to stop.")

            while self.is_running:
                try:
                    # Listen for audio with configurable timeout
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.listen_timeout,
                        phrase_time_limit=self.phrase_time_limit,
                    )

                    # Recognize speech using Google Speech Recognition
                    text = self.recognizer.recognize_google(audio)
                    print(f"Recognized: {text}")
                    self.type_text(text)

                except sr.WaitTimeoutError:
                    # No speech detected within timeout, continue listening
                    continue
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Speech recognition service error: {e}")
                    # Brief pause before retrying on service error
                    time.sleep(1)

    def start(self):
        """Start the speech recognition in a background thread."""
        if self.is_running:
            print("Already running!")
            return

        self.is_running = True
        self.listen_thread = threading.Thread(target=self.listen_and_type)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def stop(self):
        """Stop the speech recognition."""
        self.is_running = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("\nStopped listening.")


def main():
    """Main entry point for the Talk-to-Type application."""
    print("=" * 50)
    print("Welcome to Talk-to-Type!")
    print("=" * 50)
    print("\nThis tool will convert your speech to text and type it out.")
    print("Make sure you have a working microphone connected.\n")

    try:
        ttt = TalkToType()
        ttt.start()

        # Keep the main thread alive
        while ttt.is_running:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nShutting down...")
        ttt.stop()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("Thank you for using Talk-to-Type!")


if __name__ == "__main__":
    main()
