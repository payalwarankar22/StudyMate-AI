
from google import genai

from app.core.config import settings


class TranscriptionService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = "gemini-3.5-transcribe"

    def transcribe_audio(self, audio_path: str) -> str:

        audio_file = self.client.files.upload(
            file=audio_path
        )

        interaction = self.client.interactions.create(
            model=self.model,
            input=[
                {
                    "type": "audio",
                    "uri": audio_file.uri,
                    "mime_type": audio_file.mime_type,
                }
            ],
        )

        return interaction.output_text