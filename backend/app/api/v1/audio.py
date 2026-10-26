
import logging
import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.ai.transcription_service import TranscriptionService
from app.dependencies import get_current_user


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/audio",
    tags=["Audio"],
)


ALLOWED_AUDIO_EXTENSIONS = {
    ".m4a",
    ".mp3",
    ".wav",
    ".aac",
    ".ogg",
    ".flac",
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
CHUNK_SIZE = 1024 * 1024  # 1 MB


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    temp_file_path = None

    try:
        # 1. Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Audio file is required",
            )

        # 2. Validate file extension
        suffix = Path(file.filename).suffix.lower()

        if suffix not in ALLOWED_AUDIO_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported audio file format",
            )

        # 3. Create temporary file and copy upload in chunks
        with tempfile.NamedTemporaryFile(
            mode="wb",
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file_path = temp_file.name
            total_size = 0

            while True:
                chunk = await file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                # 4. Enforce the maximum file size
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "Audio file is too large. "
                            "Maximum allowed size is 100 MB."
                        ),
                    )

                temp_file.write(chunk)

        # 5. Transcribe audio
        transcription_service = TranscriptionService()

        transcript = transcription_service.transcribe_audio(
            audio_path=temp_file_path,
        )

        # 6. Return transcript
        return {
            "filename": file.filename,
            "transcript": transcript,
        }

    except HTTPException:
        raise

    except Exception:
        # Log the failure without returning internal details to the client
        logger.exception("Audio transcription failed")

        raise HTTPException(
            status_code=502,
            detail="Audio transcription service failed.",
        ) from None

    finally:
        try:
            # 7. Delete the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        except OSError:
            logger.exception("Failed to delete temporary audio file")
        finally:
            # 8. Close the uploaded file
            await file.close()
