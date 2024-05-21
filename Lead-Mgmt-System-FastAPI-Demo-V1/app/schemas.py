
from pydantic import BaseModel
from datetime import datetime
from typing import List, Union

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class LeadCreate(LeadBase):
    # other: str
    pass

class Lead(LeadBase):
    id: int
    owner_id: Union[int, None] = None
    # owner_id: int

    class Config:
        orm_mode = True

class LeadStatusBase(BaseModel):
    status: str

class LeadStatusCreate(LeadStatusBase):
    lead_id: int

class LeadStatusUpdate(LeadStatusBase):
    pass

class LeadStatus(LeadStatusBase):
    id: int
    lead_id: int
    attorney_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role: str

class User(UserBase):
    id: int
    is_active: bool
    leads: list[Lead] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None
