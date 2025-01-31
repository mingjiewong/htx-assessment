from typing import Tuple
import logging

from speech_recognition.asr_logic import transcribe_audio
from speech_recognition.model import asr_model
from api.exceptions import SpeechRecognitionError

class SpeechRecognizer:
    """Class to run speech recognition using an Automatic Speech Recognition (ASR) model.
    
    Attributes:
        asr_model: The ASR model for speech recognition.
    """
    def __init__(self, asr_model):
        """Initialize the SpeechRecognizer instance with an Automatic Speech Recognition (ASR) model.
        
        Args:
            asr_model: The ASR model for speech recognition.
        """
        self.asr_model = asr_model

    def transcribe_audio(self, file: str) -> Tuple[str, str]:
        """Transcribe the input audio file.
        
        Args:
            file (str): The audio file to be analyzed.

        Returns:
            Tuple[str, str]: A tuple containing the transcribed text and file duration.
        """
        try: 
            return transcribe_audio(file, self.asr_model)

        except Exception as e:
            logging.error(f"Speech recognition failed: {e}")
            raise SpeechRecognitionError(detail=str(e))

class SpeechRecognizerFactory:
    """Factory class to create SpeechRecognizer instances."""
    @staticmethod
    def create_speech_recognizer() -> SpeechRecognizer:
        """Create and return a new SpeechRecognizer instance.
        
        Returns:
            SpeechRecognizer: A new instance of the SpeechRecognizer class.
        """
        return SpeechRecognizer(asr_model=asr_model)