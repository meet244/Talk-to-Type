# Talk-to-Type

A speech-to-text tool that automatically types what you speak. Simply run the application, start talking, and watch your words appear on screen!

## Features

- 🎤 Real-time speech recognition
- ⌨️ Automatic text typing
- 🔧 Automatic ambient noise adjustment
- 🌐 Uses Google Speech Recognition API (free, no API key required)

## Requirements

- Python 3.7+
- Working microphone
- Internet connection (for speech recognition)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/meet244/Talk-to-Type.git
   cd Talk-to-Type
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   **Note for Linux users:** You may need to install PortAudio first:
   ```bash
   sudo apt-get install portaudio19-dev
   ```

   **Note for macOS users:** You may need to install PortAudio via Homebrew:
   ```bash
   brew install portaudio
   ```

## Usage

1. Run the application:
   ```bash
   python talk_to_type.py
   ```

2. Wait for the "Ready! Start speaking..." message

3. Click on the application where you want text to be typed (e.g., text editor, browser, etc.)

4. Start speaking - your words will be automatically typed!

5. Press `Ctrl+C` to stop the application

## How It Works

1. The application captures audio from your microphone
2. Speech is sent to Google's Speech Recognition API for transcription
3. The recognized text is automatically typed using keyboard simulation
4. The process repeats continuously until you stop the application

## Troubleshooting

### "Could not understand audio"
- Speak clearly and at a moderate pace
- Reduce background noise
- Ensure your microphone is working properly

### "Speech recognition service error"
- Check your internet connection
- The service may be temporarily unavailable, try again later

### No audio input detected
- Verify your microphone is connected and working
- Check system audio settings
- Ensure the correct microphone is set as default

## License

This project is open source and available under the MIT License