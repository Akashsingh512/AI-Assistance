# AI Personal Desktop Assistant

A modern, PySide6-based AI assistant for Windows 11 that integrates chat, voice commands, desktop automation, file summarization, and system monitoring.

## Features

- **AI Chat**: Conversational context using Google Gemini or OpenAI.
- **Voice Assistant**: Speech-to-text and text-to-speech for hands-free operations.
- **Desktop Automation**: Open websites, launch apps, take screenshots, and manage the clipboard using natural language.
- **File Assistant**: Search for files and summarize documents (PDF, DOCX, TXT) via AI.
- **System Monitor**: View CPU, RAM, Disk, and top running processes.
- **Secure Key Storage**: API keys are saved securely via the operating system's credential manager.

## How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   (Note: For voice features on Linux, you may need system packages like `espeak` and `portaudio19-dev` / `xclip`.)

2. **Launch the Application:**
   ```bash
   python main.py
   ```

3. **Configure Settings:**
   - When the application starts, click on **Settings** in the sidebar.
   - Enter your **Google Gemini** or **OpenAI API Key**.
   - Select your preferred AI Provider from the dropdown.
   - Click **Save Settings**.

4. **Start Using:**
   - Go to the **Chat** tab to ask general questions or instruct it to perform tasks (e.g., "Open Chrome").
   - Go to the **Voice Assistant** tab and click the microphone to give commands via voice.
