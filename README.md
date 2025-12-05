# **Talk-To-Type (Windows Voice Typing Automation)**

A tiny background tool that lets you **talk anywhere and it automatically types for you**.
Just move your mouse to the **top-left corner**, speak, move away your words get instantly typed.
Powered by **Groq Whisper** for fast, accurate transcription.

---

## **Features**

* 🎤 Voice-to-Text anywhere (Notepad, Chrome, VS Code, etc.)
* 🖱️ Hotspot activation (top-left = record, top-right = Win+H)
* 📋 Auto-copy + auto-paste (Ctrl+V)
* 🔇 100% silent (no console)
* ♾️ Runs in background
* ⚡ Optional auto-start with Windows

---

## **Install (Windows)**

### **1. Install Python**

Download from python.org → check **“Add Python to PATH”**

### **2. Install dependencies**

```bash
pip install pyautogui sounddevice soundfile pydub pyperclip groq
```

Install FFmpeg → add `/bin` folder to PATH.

### **3. Add your Groq API key**

In the `.py` file, replace:

```python
os.environ["GROQ_API_KEY"] = "your-key"
```

### **4. Save the script**

Create `talk-to-type.py` → paste the code → save.

---

## **Auto-Start (Optional)**

Create a file:

### `run-on-startup.bat`

```bat
@echo off
start "" pythonw "C:\path\to\talk-to-type.py"
exit
```

Place it in:

```
Win + R → shell:startup
```

It will now run automatically on every boot.

---

## **How to Use**

* Move mouse to **top-left** → start talking
* Move mouse away → it types your words
* Move to **top-right** → triggers Win+H

---

If you want an even shorter README or a copy-paste GitHub description only, just tell me.
