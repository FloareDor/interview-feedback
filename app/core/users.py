from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserCreate, UserResponse, pwd_context
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.auth import get_current_user
from app.models.user import User, UserCreate
from fastapi import Body
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create a new user with the hashed password
    db_user = User(username=user.username, password_hash=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        # Check if the error is due to a unique constraint violation
        if 'duplicate key value violates unique constraint' in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this username already exists.",
            )
        else:
            raise e  # Re-raise the exception if it's not a unique constraint violation

    return db_user

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve a user from the database by ID
    user = db.query(User).filter(User.id == user_id).first()
    return user

@router.get("/")
def hello_world():
    return {"msg":"hello, world!"}

@router.get("/health-check")
def hello_world():
    return {"status":"ok"}

@router.get("/protected-endpoint")
def hello_world(current_user: User = Depends(get_current_user)):
    return {"status":"ok"}

# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not user.verify_password(form_data.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(user_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()

    if not user or not user.verify_password(user_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}