from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
# from app.models.page import Page, PageResponse
from typing import List
from app.auth import get_current_user
from app.models.user import User
from sqlalchemy import distinct
from app.models.interview import Interview

router = APIRouter()

@router.get("/get-all-pages", response_model=List[str])
def get_all_pages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id

    page_ids = db.query(distinct(Interview.page_id)).filter(Interview.interviewer_id == user_id).all()
    
    # Convert the result to a list of strings
    page_ids = [str(page_id[0]) for page_id in page_ids]

    return page_ids