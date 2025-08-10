from sqlalchemy.orm import Session
import model, schemas
import uuid
from sqlalchemy import func
from datetime import datetime, timedelta

def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = model.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead