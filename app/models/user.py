from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel
from passlib.context import CryptContext
from bson import ObjectId
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class User(Base):
    __tablename__ = "users"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(ObjectId()))
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    interviews_conducted = relationship("Interview", back_populates="interviewer")
    # password = Column(String)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True