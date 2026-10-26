from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import tempfile
import os

from app.ai.transcription_service import TranscriptionService
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)


ALLOWED_AUDIO_EXTENSIONS = {
    ".m4a",
    ".mp3",
    ".wav",
    ".aac",
    ".ogg",
    ".flac"
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    # 1. Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio file is required"
        )

    # 2. Validate file extension
    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio file format"
        )

    temp_file_path = None
    total_size = 0

    try:

        # 3. Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file_path = temp_file.name

            # 4. Copy file in chunks
            while True:

                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                # 5. Validate file size
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file is too large. Maximum allowed size is 100 MB."
                    )

                temp_file.write(chunk)

        # 6. Transcribe audio
        transcription_service = TranscriptionService()

        transcript = transcription_service.transcribe_audio(
            audio_path=temp_file_path
        )

        # 7. Return transcript
        return {
            "filename": file.filename,
            "transcript": transcript
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            f"Audio transcription error: "
            f"{type(e).__name__}: {e}"
        )

        raise HTTPException(
            status_code=502,
            detail="Audio transcription service failed."
        )

    finally:

        # 8. Always delete temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
