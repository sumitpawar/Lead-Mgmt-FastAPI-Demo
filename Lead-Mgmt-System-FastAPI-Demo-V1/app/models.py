
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    availability = Column(Boolean, default=True)

    leads = relationship("Lead", back_populates="owner")

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True) 
    resume = Column(LargeBinary)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="leads")
    statuses = relationship("LeadStatus", back_populates="lead")

class LeadStatus(Base):
    __tablename__ = "lead_statuses"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id")) 
    status = Column(String)
    attorney_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    lead = relationship("Lead", back_populates="statuses")