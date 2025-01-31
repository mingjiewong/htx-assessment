import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .logging_config import LOGGING_CONFIG
from .routes import router
from .middleware import UUIDMiddleware
from .exceptions import (
    SpeechRecognitionError,
    speech_recognition_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and shutdown events.

    Args:
        app: The FastAPI application instance.
    """
    # Startup actions
    logger.info("Speech Recognition API is starting up...")
    
    # Yield control to the application
    try:
        yield
    finally:
        # Shutdown actions
        logger.info("Speech Recognition API is shutting down...")

app = FastAPI(
    title="Speech Recognition API",
    description="API for speech recognition.",
    version="1.0.0",
    lifespan=lifespan
)

# Add the UUID middleware
app.add_middleware(UUIDMiddleware)

# Register the custom validation exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Register the custom exception handler for Speech Recognition errors
app.add_exception_handler(SpeechRecognitionError, speech_recognition_exception_handler)

# Register the generic exception for all other exceptions
app.add_exception_handler(Exception, generic_exception_handler)

# Include your API router
app.include_router(router)