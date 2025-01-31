from enum import Enum

class ErrorDescriptions(Enum):
    """Enum class to define multiple error descriptions."""

    INVALID_INPUT_ERROR = "Please ensure the payload adheres to the required format."
    INTERNAL_SERVER_ERROR = "An internal server error occurred. Please try again later."
    SPEECH_RECOGNITION_ERROR = "An error occurred during speech recognition. Please try again later"