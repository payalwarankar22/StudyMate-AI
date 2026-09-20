
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class Note(Base):
    __tablename__= "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable= False
    )


    updated_at = Column(
        DateTime(timezone.utc),
        default= lambda: datetime.now(timezone.utc),
        onupdate= lambda: datetime.now(timezone.utc),
        nullable= False

    )


    user = relationship("User", back_populates="notes")

    
