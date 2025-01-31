import logging
import os

from fastapi import APIRouter, Depends, Request, UploadFile, File
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.factory import SpeechRecognizer

from .dependencies import get_speech_recognizer
from .schemas import Transcription
from .exceptions import SpeechRecognitionError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Speech Recognition"],
    )

@router.get("/ping")
async def health_check() -> str:
    """Endpoint to check the health of the API.
    
    Returns:
        str: A simple "pong" response to indicate that the API is healthy.
    """
    return JSONResponse(content="pong", status_code=200)

@router.post("/asr", response_model=Transcription)
async def run_asr(
    request: Request, 
    file: UploadFile = File(...), 
    speech_recognizer: SpeechRecognizer = Depends(get_speech_recognizer)
    ) -> Transcription:
    """Endpoint for speech recognition on input file.
    
    Args:
        request: The incoming request object.
        file: The input file for speech recognition.
        speech_recognizer: The SpeechRecognizer instance provided by dependency injection.
    
    Returns:
        Transcription: A response containing transcribed text, duration, and request ID.

    Raises:
        RequestValidationError: If the input file is empty or not in the expected format.
        SpeechRecognitionError: If an error occurs during speech recognition.
    """
    request_id = request.state.request_id
    logger.info(f"Request ID {request_id}: Received speech recognition request.")

    try:
        # Save the uploaded file to a temporary location
        file_location = os.path.join("data", file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Perform speech recognition
        transcription, duration = speech_recognizer.transcribe_audio(file_location)
        logger.info(f"Request ID {request_id}: Speech recognition successful.")
        
        # Optionally, remove the file after processing
        os.remove(file_location)

        # Return the transcribed text along with file duration and request_id
        return Transcription(
            transcription=transcription, 
            duration=duration,
            request_id=request.state.request_id
            )

    except RequestValidationError as e:
        logger.error(f"Request ID {request_id}: {e}")
        # Propagate the except to be handled by the custom exception handler
        raise e
    
    except SpeechRecognitionError as e:
        logger.error(f"Request ID {request_id}: {e}")
        # Propagate the except to be handled by the custom exception handler
        raise e
    
    except Exception as e:
        logger.error(f"Request ID {request_id}: {e}")
        # Propagate the exception to be handled by the generic exception handler
        raise e