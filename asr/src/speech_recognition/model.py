from transformers import pipeline

from core.config import settings

# Initialize asr model
asr_model = pipeline(
    "automatic-speech-recognition",
    model=settings.MODEL_NAME
)

