from pydantic import BaseModel

class BaseResponse(BaseModel):
    """Base schema to represent the response structure for speech recognition.

    Attributes:
        request_id (str): The unique identifier for the request.
    """
    request_id: str

class Transcription(BaseResponse):
    """Schema to represent the response structure for speech recognition.
    
    Attributes:
        transcription (str): The transcribed text from the file.
        duration (str): The duration of the file.
    """
    transcription: str
    duration: str