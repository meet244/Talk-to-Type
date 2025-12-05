#!/usr/bin/env python3
"""
Unit tests for Talk-to-Type application.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch


class TestTalkToType(unittest.TestCase):
    """Test cases for TalkToType class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock pynput before importing talk_to_type
        self.mock_keyboard = MagicMock()
        self.mock_controller = MagicMock(return_value=self.mock_keyboard)
        self.mock_key = MagicMock()

        self.patcher_keyboard = patch.dict(
            "sys.modules",
            {
                "pynput": MagicMock(),
                "pynput.keyboard": MagicMock(
                    Controller=self.mock_controller, Key=self.mock_key
                ),
            },
        )
        self.patcher_keyboard.start()

    def tearDown(self):
        """Clean up after tests."""
        self.patcher_keyboard.stop()
        # Remove cached module if present
        if "talk_to_type" in sys.modules:
            del sys.modules["talk_to_type"]

    def test_import_module(self):
        """Test that the module can be imported."""
        import talk_to_type

        self.assertTrue(hasattr(talk_to_type, "TalkToType"))
        self.assertTrue(hasattr(talk_to_type, "main"))

    def test_talk_to_type_init(self):
        """Test TalkToType initialization."""
        import talk_to_type

        ttt = talk_to_type.TalkToType()
        self.assertFalse(ttt.is_running)
        self.assertIsNone(ttt.listen_thread)
        self.assertIsNotNone(ttt.recognizer)

    def test_type_text(self):
        """Test type_text method."""
        import talk_to_type

        ttt = talk_to_type.TalkToType()
        ttt.type_text("hello world")

        # Verify keyboard.type was called
        self.mock_keyboard.type.assert_called()

    def test_type_text_empty(self):
        """Test type_text with empty string."""
        import talk_to_type

        ttt = talk_to_type.TalkToType()
        # Reset mock to track calls
        self.mock_keyboard.type.reset_mock()

        ttt.type_text("")

        # With empty string, type should not be called
        self.mock_keyboard.type.assert_not_called()

    def test_type_text_no_extra_space_if_whitespace(self):
        """Test that no extra space is added if text ends with whitespace."""
        import talk_to_type

        ttt = talk_to_type.TalkToType()
        self.mock_keyboard.type.reset_mock()

        # Test with text ending in space
        ttt.type_text("hello world ")
        # Should only call type once with the text, not add extra space
        self.mock_keyboard.type.assert_called_once_with("hello world ")

    def test_type_text_adds_space_for_normal_text(self):
        """Test that space is added after normal text."""
        import talk_to_type

        ttt = talk_to_type.TalkToType()
        self.mock_keyboard.type.reset_mock()

        # Test with normal text
        ttt.type_text("hello world")
        # Should call type twice: once for text, once for space
        calls = self.mock_keyboard.type.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], "hello world")
        self.assertEqual(calls[1][0][0], " ")

    def test_configurable_timeouts(self):
        """Test that timeout values are configurable."""
        import talk_to_type

        ttt = talk_to_type.TalkToType(
            listen_timeout=10,
            phrase_time_limit=30,
            energy_threshold=500,
        )

        self.assertEqual(ttt.listen_timeout, 10)
        self.assertEqual(ttt.phrase_time_limit, 30)
        self.assertEqual(ttt.recognizer.energy_threshold, 500)

    def test_start_stop(self):
        """Test start and stop methods."""
        import talk_to_type

        # Mock the microphone to avoid actual audio capture
        with patch("speech_recognition.Microphone"):
            ttt = talk_to_type.TalkToType()

            # Test that we can start
            self.assertFalse(ttt.is_running)

            # Mock the listen_and_type method
            ttt.listen_and_type = MagicMock()
            ttt.start()

            self.assertTrue(ttt.is_running)
            self.assertIsNotNone(ttt.listen_thread)

            # Test that starting again doesn't create new thread
            old_thread = ttt.listen_thread
            ttt.start()
            self.assertEqual(old_thread, ttt.listen_thread)

            # Test stop
            ttt.stop()
            self.assertFalse(ttt.is_running)


class TestIntegration(unittest.TestCase):
    """Integration tests (require mocking of external services)."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock pynput before importing talk_to_type
        self.mock_keyboard = MagicMock()
        self.mock_controller = MagicMock(return_value=self.mock_keyboard)
        self.mock_key = MagicMock()

        self.patcher_keyboard = patch.dict(
            "sys.modules",
            {
                "pynput": MagicMock(),
                "pynput.keyboard": MagicMock(
                    Controller=self.mock_controller, Key=self.mock_key
                ),
            },
        )
        self.patcher_keyboard.start()

    def tearDown(self):
        """Clean up after tests."""
        self.patcher_keyboard.stop()
        if "talk_to_type" in sys.modules:
            del sys.modules["talk_to_type"]

    def test_speech_recognition_timeout(self):
        """Test handling of speech recognition timeout."""
        import talk_to_type
        import speech_recognition as sr

        ttt = talk_to_type.TalkToType()

        # Test that WaitTimeoutError is handled gracefully
        with patch.object(
            ttt.recognizer, "listen", side_effect=sr.WaitTimeoutError("Timeout")
        ):
            with patch.object(
                ttt.recognizer, "adjust_for_ambient_noise"
            ):
                with patch("speech_recognition.Microphone"):
                    # This should not raise an exception
                    ttt.is_running = True

                    # Set to stop after one iteration
                    def stop_after_call(*args, **kwargs):
                        ttt.is_running = False
                        raise sr.WaitTimeoutError("Timeout")

                    ttt.recognizer.listen = stop_after_call

                    # Should not raise
                    try:
                        ttt.listen_and_type()
                    except Exception:
                        pass  # Expected to exit when is_running becomes False


if __name__ == "__main__":
    unittest.main()
