import logging

from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .constants import ErrorDescriptions

logger = logging.getLogger(__name__)

class SpeechRecognitionError(HTTPException):
    """Custom exception for speech recognition failures.
    
    Attributes:
        detail (str): A description of the error.
    """
    def __init__(self, detail: str = ErrorDescriptions.SPEECH_RECOGNITION_ERROR.value):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            headers={"X-Error-Code": "SPEECH_RECOGNITION_ERROR"}
        )

def build_error_response(
        request: Request, 
        error_code: str, 
        message: str, 
        status_code: int
    ) -> JSONResponse:
    """Constructs a standardized JSON error response.

    Args:
        request (Request): The incoming request object.
        error_code (str): A unique error code identifying the error type.
        message (str): A descriptive error message.
        status_code (int): The HTTP status code for the response.

    Returns:
        JSONResponse: A JSON response containing error details and the request ID.
    """
    request_id = request.state.request_id
    logger.error(f"Request ID {request_id}: {message}")
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message
            },
            "request_id": request_id
        }
    )

async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
    """Handler for RequestValidationError.

    Args:
        request: The incoming request object.
        exc: The exception instance.

    Returns:
        JSONResponse: A JSON response with error details.
    """
    return build_error_response(
        request=request,
        error_code="INVALID_INPUT_ERROR",
        message=ErrorDescriptions.INVALID_INPUT_ERROR.value,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

async def generic_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
    """Handler for all uncaught exceptions.

    Args:
        request: The incoming request object.
        exc: The exception instance.

    Returns:
        JSONResponse: A JSON response with error details.
    """
    return build_error_response(
        request=request,
        error_code="INTERNAL_SERVER_ERROR",
        message=ErrorDescriptions.INTERNAL_SERVER_ERROR.value,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

async def speech_recognition_exception_handler(
        request: Request,
        exc: SpeechRecognitionError
    ) -> JSONResponse:
    """Handler for SpeechRecognitionError.

    Args:
        request: The incoming request object.
        exc: The exception instance.

    Returns:
        JSONResponse: A JSON response with error details.
    """
    return build_error_response(
        request=request,
        error_code="SPEECH_RECOGNITION_ERROR",
        message=exc.detail,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )