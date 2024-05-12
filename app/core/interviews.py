from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.interview import Interview, InterviewCreate, InterviewUpdate, InterviewResponse
from typing import List
from app.auth import get_current_user
from app.models.user import User
# from app.models.page import Page, PageCreate

router = APIRouter()

# @router.post("/add-interview", response_model=InterviewResponse)
# def create_interview(interview: InterviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_interview = Interview(**interview.dict())
#     db.add(db_interview)
#     db.commit()
#     db.refresh(db_interview)
#     return db_interview

@router.post("/add-interview", response_model=InterviewResponse)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    db_interview = Interview(**interview.dict(), interviewer_id=user_id)
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    return db_interview

@router.put("/update-interview", response_model=InterviewResponse)
def update_interview(interview: InterviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    db_interview = db.query(Interview).filter(Interview.id == interview.id, Interview.interviewer_id == user_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    update_data = interview.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_interview, key, value)
    db.commit()
    db.refresh(db_interview)
    return db_interview

@router.delete("/delete-interview")
def delete_interview(interview: InterviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    db_interview = db.query(Interview).filter(Interview.id == interview.id, Interview.interviewer_id == user_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    db.delete(db_interview)
    db.commit()
    return {"message": "Interview deleted successfully"}

@router.get("/get-all-interviews/{page_id}", response_model=List[InterviewResponse])
def get_interviews(page_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id  # Get the user_id from the authenticated user object
    print(user_id, page_id)
    interviews = db.query(Interview).filter(Interview.page_id == page_id, Interview.interviewer_id == user_id).all()
    return interviews

@router.get("/get-interview/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    interview = db.query(Interview).filter(Interview.id == interview_id, Interview.interviewer_id == user_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview