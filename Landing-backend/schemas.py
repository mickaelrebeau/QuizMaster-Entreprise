from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None
    form_type: str

class LeadCreate(LeadBase):
    pass