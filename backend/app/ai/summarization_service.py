from app.ai.gemini_service import GeminiService


class SummarizationService:

    def __init__(self):
        self.gemini_service = GeminiService()

    def summarize_note(self, note_content: str) -> str:

        prompt = f"""
Summarize the following study note clearly and concisely.

Keep the important concepts and key information.
Do not add information that is not present in the note.

Study Note:
{note_content}

Summary:
"""

        return self.gemini_service.generate_content(prompt)

    