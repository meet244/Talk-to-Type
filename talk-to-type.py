import os
import sys
import time
import threading
import queue
import tempfile

# Redirect stdout and stderr to devnull to suppress console messages
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import pyautogui
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
import pyperclip
from groq import Groq  # Ensure you have installed the Groq client library

# Disable the fail-safe feature
pyautogui.FAILSAFE = False

# Set the Groq API key as an environment variable
os.environ["GROQ_API_KEY"] = "Your_GROQ_API_KEY_HERE"

# Global settings for audio recording
SAMPLERATE = 44100  # Sample rate in Hz
CHANNELS = 1        # Mono recording

def record_audio(wav_filename, stop_event):
    """Record audio to a WAV file until stop_event is set."""
    q = queue.Queue()

    def audio_callback(indata, frames, time_info, status):
        # Suppress status logs
        q.put(indata.copy())

    with sf.SoundFile(wav_filename, mode='w', samplerate=SAMPLERATE, channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, callback=audio_callback):
            while not stop_event.is_set():
                try:
                    data = q.get(timeout=0.1)
                    file.write(data)
                except queue.Empty:
                    continue

def main():
    # Positions that trigger actions (you can adjust these values)
    recording_pos = (0, 0)      # Mouse position to trigger voice recording
    edge_launch_pos = (1919, 0) # Mouse position to trigger launching Edge
    check_interval = 0.1        # Check the mouse every 0.1 seconds
    dwell_time = 0.5              # Mouse must remain at the position for 0.5 seconds to trigger

    # Flag to track whether Edge has been launched in the current dwell session
    edge_launched = False

    while True:
        # Check if screen is effectively off (size becomes 0)
        try:
            if pyautogui.size()[0] == 0:
                time.sleep(1)
                continue
        except Exception:
            time.sleep(1)
            continue

        current_pos = pyautogui.position()
        
        # Trigger recording if the mouse is at the recording position
        if current_pos == recording_pos:
            start_time = time.time()
            while time.time() - start_time < dwell_time:
                if pyautogui.position() != recording_pos:
                    break
                time.sleep(check_interval)
            else:
                # Start recording process
                with tempfile.TemporaryDirectory() as temp_dir:
                    wav_filename = os.path.join(temp_dir, "audio.wav")
                    m4a_filename = os.path.join(temp_dir, "audio.m4a")
                    
                    stop_event = threading.Event()
                    record_thread = threading.Thread(target=record_audio, args=(wav_filename, stop_event))
                    record_thread.start()
                    
                    # Record until the mouse leaves the recording position
                    while True:
                        if pyautogui.position() != recording_pos:
                            stop_event.set()
                            break
                        time.sleep(check_interval)
                    record_thread.join()
                    
                    # Convert recorded WAV to m4a
                    try:
                        sound = AudioSegment.from_wav(wav_filename)
                        sound.export(m4a_filename, format="mp4")
                    except Exception:
                        continue

                    # Send the audio file to Groq for transcription
                    try:
                        client = Groq()
                        with open(m4a_filename, "rb") as file:
                            transcription = client.audio.transcriptions.create(
                                file=(os.path.basename(m4a_filename), file.read()),
                                model="whisper-large-v3-turbo",
                                temperature=0.5,
                            )
                        text = transcription.text
                    except Exception:
                        continue

                    # Copy the transcription text to the clipboard
                    pyperclip.copy(text)
                    # Press Ctrl+V to paste the text
                    pyautogui.hotkey('ctrl', 'v')

                # Allow a brief pause before resuming monitoring
                time.sleep(1)
        
        # Launch Edge if the mouse is at the edge launch position
        elif current_pos == edge_launch_pos and not edge_launched:
            start_time = time.time()
            while time.time() - start_time < dwell_time:
                if pyautogui.position() != edge_launch_pos:
                    break
                time.sleep(check_interval)
            else:
                # Press Windows+H to launch Edge
                pyautogui.hotkey('win', 'h')
                edge_launched = True
                
                # Wait until the cursor moves away from the position
                while pyautogui.position() == edge_launch_pos:
                    time.sleep(check_interval)
                
                # Reset the flag once the cursor has moved away
                edge_launched = False
        
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
