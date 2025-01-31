from pydub import AudioSegment

from typing import List, Dict, Any, Tuple, Callable

def get_audio_duration(
        file_path: str,
        time_unit: int = 1000,
        decimal_places: int = 1
    ) -> float:
    """Get the duration of an audio file in seconds.
    
    Args:
        file_path (str): The path to the audio file.
        time_unit (int): The time unit to convert the duration to (default is 1000 for seconds).
        decimal_places (int): The number of decimal places to round the duration to (default is 1).

    Returns:
        float: The duration of the audio file in seconds.
    """
    audio = AudioSegment.from_file(file_path)
    duration_seconds = len(audio) / time_unit  # Convert to specified time unit
    duration_seconds = round(duration_seconds, decimal_places) # Round to specified decimal places
    return duration_seconds

def transcribe_audio(
        file_path: str, 
        asr_model: Callable[[str], List[Dict[str, Any]]]
    ) -> Tuple[str, str]:
    """Transcribe the input audio file.
    
    Args:
        file_path (str): The audio file to be transcribed.
        asr_model (Callable): The ASR model for speech recognition.

    Returns:
        Tuple[str, str]: A tuple containing the transcribed text and file duration.
    """

    # Perform speech recognition
    transcription = asr_model(file_path)

    # Get the duration of the audio file
    duration = get_audio_duration(file_path)

    return transcription.get('text', ''), str(duration)