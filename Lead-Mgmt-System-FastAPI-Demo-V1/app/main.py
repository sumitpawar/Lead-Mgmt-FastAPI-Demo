from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Annotated
import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI 
app = FastAPI(
    title="Lead Management System",
    description="An application to manage leads for attorneys",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, crud.SECRET_KEY, algorithm=crud.ALGORITHM)
    return encoded_jwt

# Verify password
def verify_password(plain_password, hashed_password):
    is_verified = pwd_context.verify(plain_password, hashed_password)
    # print("is_verified: ", is_verified)
    return is_verified

# password hash
def get_password_hash(password):
    return pwd_context.hash(password)

# Authenticate user
def authenticate_user(db, email: str, password: str):
    # print("authenticate_user: email: ", email, ", password: ", password)
    user = crud.get_user_by_email(db, email)
    # print("authenticate_user: user: ", user)
    # print("get_password_hash: ", get_password_hash('password'))
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Get current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        # print("payload: ", payload)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Default
@app.get("/")
async def default():
    return {"Welcome to Lead Management System - Version 1.0.0"}

# Create lead
@app.post("/leads/", response_model=schemas.Lead)
async def create_lead(background_tasks: BackgroundTasks, db: Session = Depends(get_db), lead: schemas.LeadCreate = Depends(), resume: UploadFile = File()):
    #print(resume.file.read())
    db_lead = crud.create_lead(db=db, lead=lead, resume=resume)
    background_tasks.add_task(crud.send_emails, db=db, lead=db_lead)
    return db_lead

# Get leads
@app.get("/leads/", response_model=list[schemas.Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    leads = crud.get_leads(db, skip=skip, limit=limit)
    return leads

# Update lead status
@app.put("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead(lead_id: int, lead_status: schemas.LeadStatusUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)): #current_user: Annotated[schemas.User, Depends(get_current_user)]):
    db_lead = crud.update_lead_owner(db, lead_id, current_user.id)
    return crud.update_lead_status(db, lead_id, lead_status, current_user.id)

# Authenticate user
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/attorneys/{attorney_id}/available")
def mark_attorney_available(attorney_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if current_user.id != attorney_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update availability")
    
    attorney = db.query(models.User).filter(models.User.id == attorney_id).first()
    if not attorney:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attorney not found")
    
    attorney.availability = True
    db.commit()
    return {"message": "Attorney marked as available"}
