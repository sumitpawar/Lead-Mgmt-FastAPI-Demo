
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
import models, schemas, utils
from fastapi import UploadFile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "b91a3d6955fe8758801cd70ec28aec1569e4fc760bc3a2623b4b2a9a61422158"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create lead
def create_lead(db: Session, lead: schemas.LeadCreate, resume: UploadFile):
    #hashed_password = pwd_context.hash(lead.password)
    db_lead = models.Lead(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        resume=resume.file.read()
        # resume=b'This is a test123'
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    # Create lead status
    lead_status = models.LeadStatus(
        lead_id=db_lead.id,
        status="PENDING"
    )
    db.add(lead_status)
    db.commit()

    return db_lead

# Send Emails
def send_emails(db: Session, lead: models.Lead):
    # Send email to prospect
    utils.send_email(lead.email, "Thank you for your interest", "We have received your application and will review it shortly.")
    
    # Send email to attorney
    #attorney = get_attorney(db)
    #utils.send_email(attorney.email, "New Lead", f"A new lead has been submitted by {lead.first_name} {lead.last_name}.")
    
    # Get the list of available attorneys
    attorneys = db.query(models.User).filter(
        models.User.role == "attorney",
        models.User.availability == True
    ).all()

    if attorneys:
        # Select the attorney with the least number of active leads
        attorney = min(attorneys, key=lambda a: db.query(models.LeadStatus).filter(models.LeadStatus.attorney_id == a.id, models.LeadStatus.status == "PENDING").count())
        
        utils.send_email(attorney.email, "New Lead", f"A new lead has been submitted by {lead.first_name} {lead.last_name}.")
        attorney.availability = False
        db.commit()
    else:
        # Handle case when no attorney is available
        print("No available attorney found.")


# Get leads
def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).offset(skip).limit(limit).all()

# Update lead status
def update_lead_status(db: Session, lead_id: int, lead_status: schemas.LeadStatusUpdate, attorney_id: int):
    db_lead_status = db.query(models.LeadStatus).filter(models.LeadStatus.lead_id == lead_id).first()
    db_lead_status.status = lead_status.status
    db_lead_status.attorney_id = attorney_id
    db_lead_status.updated_at = datetime.now()
    db.commit()
    db.refresh(db_lead_status)
    return db_lead_status

# Update lead owner
def update_lead_owner(db: Session, lead_id: int, attorney_id: int):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    db_lead.owner_id = attorney_id
    db_lead.updated_at = datetime.now()
    db.commit()
    db.refresh(db_lead)
    return db_lead

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Get attorney
def get_attorney(db: Session):
    return db.query(models.User).filter(models.User.role == "attorney").first()

# Get first available attorney
def get_first_available_attorney(db: Session):
    return db.query(models.User).filter(
        models.User.role == "attorney",
        models.User.availability == True
    ).first()
