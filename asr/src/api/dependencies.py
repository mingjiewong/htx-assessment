import logging

from core.factory import SpeechRecognizerFactory, SpeechRecognizer

logger = logging.getLogger(__name__)

def get_speech_recognizer() -> SpeechRecognizer:
    """Factory function to create a new automatic speech recognition instance for dependency injection.

    This function serves as a FastAPI dependency to provide a speech recognition instance to the endpoint.
    It ensures that a new SpeechRecognizer instance is created and returned for each request to maintain
    thread safety in concurrent environments. This approach also encourages separation of concerns
    by isolating object creation logic from route handlers.

    Returns:
        SpeechRecognizer: An instance of the SpeechRecognizer class configured for speech recognition.

    Example:
        @router.post("/asr")
        async def run_asr(
            request: Request,
            file: UploadFile,
            speech_recognizer: SpeechRecognizer = Depends(get_speech_recognizer)
        ):
            # Endpoint logic to run speech recognition
            transcription, duration = speech_recognizer.transcribe_audio(file)
            return {"transcription": transcription, "duration": duration}
    """
    logger.debug("Creating a new SpeechRecognizer instance.")
    return SpeechRecognizerFactory.create_speech_recognizer()