from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"))
    interviewee_name = Column(String)
    interviewee_id = Column(Integer)
    status = Column(String)
    feedback = Column(String)
    rating = Column(Integer)

    page = relationship("Page", back_populates="interviews")