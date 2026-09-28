from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.database import get_db
from backend.models import Lead, AdminUser
from backend.schemas import LeadCreate, LeadUpdate, LeadResponse
from backend.security import get_current_admin

router = APIRouter(prefix="/api/leads", tags=["Leads"])

@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    new_lead = Lead(
        name=payload.name,
        email=payload.email,
        message=payload.message,
        status="new"
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@router.get("", response_model=List[LeadResponse])
def get_leads(
    search: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    query = db.query(Lead)
    if status_filter:
        query = query.filter(Lead.status == status_filter)
    if search:
        search_fmt = f"%{search}%"
        query = query.filter(
            or_(
                Lead.name.ilike(search_fmt),
                Lead.email.ilike(search_fmt),
                Lead.message.ilike(search_fmt)
            )
        )
    leads = query.order_by(Lead.created_at.desc()).all()
    return leads

@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead_by_id(
    lead_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    payload: LeadUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if payload.name is not None:
        lead.name = payload.name
    if payload.email is not None:
        lead.email = payload.email
    if payload.message is not None:
        lead.message = payload.message
    if payload.status is not None:
        if payload.status not in ["new", "contacted", "qualified", "converted", "closed"]:
            raise HTTPException(status_code=400, detail="Invalid lead status")
        lead.status = payload.status

    lead.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    return lead

@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return None
