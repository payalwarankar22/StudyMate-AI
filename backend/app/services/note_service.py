
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note


class NoteService:

    # Create Note
    def create_note(
        self,
        db: Session,
        title: str,
        content: str,
        user_id: int
    ) -> Note:

        new_note = Note(
            title=title,
            content=content,
            user_id=user_id
        )

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        return new_note


#########################################################################
    # Get all notes for current user

    def get_my_notes(
        self,
        db: Session,
        user_id: int
    ) -> list[Note]:

        statement = (
            select(Note)
            .where(Note.user_id == user_id)
        )

        result = db.execute(statement)

        return list(result.scalars().all())



###################################################################################################
    # Get Note by ID for current user

    def get_note_by_id(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ) -> Note | None:

        statement = (
            select(Note)
            .where(
                Note.id == note_id,
                Note.user_id == user_id
            )
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()



######################################################################################################
    # Update Note

    def update_note(
        self,
        db: Session,
        note_id: int,
        title: str,
        content: str,
        user_id: int
    ) -> Note | None:

        statement = (
            select(Note)
            .where(
                Note.id == note_id,
                Note.user_id == user_id
            )
        )

        result = db.execute(statement)

        note = result.scalar_one_or_none()

        if note is None:
            return None

        note.title = title
        note.content = content

        db.commit()
        db.refresh(note)

        return note


####################################################################################################
    # Delete Note

    def delete_note(
        self,
        db: Session,
        note_id: int,
        user_id: int
    ) -> Note | None:

        statement = (
            select(Note)
            .where(
                Note.id == note_id,
                Note.user_id == user_id
            )
        )

        result = db.execute(statement)

        note = result.scalar_one_or_none()

        if note is None:
            return None

        db.delete(note)
        db.commit()

        return note

