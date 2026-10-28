import pyttsx3
import threading

class TextToSpeech:
    def __init__(self):
        self.engine = None
        self._init_engine()
        
    def _init_engine(self):
        try:
            self.engine = pyttsx3.init()
            # Try to find a good English voice
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            self.engine.setProperty('rate', 170)
        except Exception as e:
            print(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def speak(self, text: str):
        if not self.engine:
            return
            
        def _run_speak():
            try:
                # To prevent errors if speak is called while already speaking
                # we wrap it in a fresh instance if needed, or handle exception.
                # However, pyttsx3 can be tricky with threads. We initialize a new engine
                # in the thread to ensure thread safety across OSs.
                local_engine = pyttsx3.init()
                local_engine.setProperty('rate', 170)
                local_engine.say(text)
                local_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")

        # Run TTS in a daemon thread so it doesn't block UI
        threading.Thread(target=_run_speak, daemon=True).start()
