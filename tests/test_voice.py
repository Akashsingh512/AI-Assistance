import pytest
from app.voice.text_to_speech import TextToSpeech
from app.voice.speech_to_text import SpeechToText

def test_speech_to_text_init():
    stt = SpeechToText()
    assert stt.recognizer is not None

def test_text_to_speech_init():
    tts = TextToSpeech()
    # It might fail to init if no audio drivers in CI, but object should exist
    assert hasattr(tts, 'engine') 
