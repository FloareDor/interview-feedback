from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    interviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    page_id = Column(Integer)
    # interviewee_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    interviewee_name = Column(String)
    status = Column(String)
    feedback = Column(String)
    rating = Column(Integer)

    # page = relationship("Page", back_populates="interviews")
    interviewer = relationship("User", back_populates="interviews_conducted")

class InterviewCreate(BaseModel):
    page_id: int
    interviewee_name: str
    status: str
    feedback: str
    rating: int
    # interviewee_id: uuid.UUID = uuid.uuid4()

class InterviewUpdate(BaseModel):
    id: int
    page_id: int | None = None
    interviewee_name: str | None = None
    # interviewee_id: uuid.UUID | None = None
    status: str | None = None
    feedback: str | None = None
    rating: int | None = None

class InterviewResponse(BaseModel):
    id: int
    page_id: int
    interviewee_name: str
    # interviewee_id: uuid.UUID
    status: str
    feedback: str
    rating: int
    interviewer_id: int

    class Config:
        from_attributes = True