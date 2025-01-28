from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Settings for the speech recognition API.

    Attributes:
        DEBUG (bool): Flag to enable debug mode.
        MODEL_NAME (str): The name of the pre-trained model in huggingface to use for speech recognition.
        LOG_FILE (str): Path to the log file to store application logs.
    """
    # Define the settings attributes with default values
    DEBUG: bool = False
    MODEL_NAME: str = "facebook/wav2vec2-large-960h"
    LOG_FILE: str = "logs/app.log"

    # Load environment variables from the .env file
    model_config = ConfigDict(env_file=".env", extra="allow")

# Create an instance of the Settings class to be used throughout the application
settings = Settings()