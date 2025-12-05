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

    def __init__(self):
        """Initialize the speech recognizer and keyboard controller."""
        self.recognizer = sr.Recognizer()
        self.keyboard = Controller()
        self.is_running = False
        self.listen_thread = None

        # Adjust for ambient noise sensitivity
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    def type_text(self, text):
        """Type the given text using the keyboard controller.

        Args:
            text: The text string to type.
        """
        if text:
            self.keyboard.type(text)
            # Add a space after each phrase for natural typing
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
                    # Listen for audio with a timeout
                    audio = self.recognizer.listen(
                        source, timeout=5, phrase_time_limit=10
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
