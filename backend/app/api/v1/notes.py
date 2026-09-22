from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.services.note_service import NoteService
from app.dependencies import get_current_user
from app.ai.summarization_service import SummarizationService


router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


################################################################
# Post route (Create note)

@router.post("/", response_model=NoteResponse)
def create_note(
    request: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = NoteService()

    note = service.create_note(
        db=db,
        title=request.title,
        content=request.content,
        user_id=current_user.id
    )

    return note


################################################################################
# Get Notes route (Getting the notes)

@router.get("/", response_model=list[NoteResponse])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = NoteService()

    notes = service.get_my_notes(
        db=db,
        user_id=current_user.id
    )

    return notes


#########################################################################
# Get Notes by id route (Getting note by id)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note_by_id(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = NoteService()

    note = service.get_note_by_id(
        db=db,
        note_id=note_id,
        user_id=current_user.id
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


########################################################################
# Put request (Update Note)

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    request: NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = NoteService()

    note = service.update_note(
        db=db,
        note_id=note_id,
        title=request.title,
        content=request.content,
        user_id=current_user.id
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


######################################################################################################
# Delete Note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = NoteService()

    note = service.delete_note(
        db=db,
        note_id=note_id,
        user_id=current_user.id
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return {
        "message": "Note deleted successfully"
    }


######################################################################################################
# AI Summarize Note

@router.post("/{note_id}/summarize")
def summarize_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    note_service = NoteService()

    note = note_service.get_note_by_id(
        db=db,
        note_id=note_id,
        user_id=current_user.id
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    summarization_service = SummarizationService()

    summary = summarization_service.summarize_note(
        note_content=note.content
    )

    return {
        "note_id": note.id,
        "summary": summary
    }