from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Lead, Project, AdminUser
from backend.schemas import AnalyticsOverview
from backend.security import get_current_admin

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    total_leads = db.query(func.count(Lead.id)).scalar() or 0
    new_leads = db.query(func.count(Lead.id)).filter(Lead.status == "new").scalar() or 0
    contacted_leads = db.query(func.count(Lead.id)).filter(Lead.status == "contacted").scalar() or 0
    qualified_leads = db.query(func.count(Lead.id)).filter(Lead.status == "qualified").scalar() or 0
    converted_leads = db.query(func.count(Lead.id)).filter(Lead.status == "converted").scalar() or 0
    closed_leads = db.query(func.count(Lead.id)).filter(Lead.status == "closed").scalar() or 0

    total_projects = db.query(func.count(Project.id)).scalar() or 0

    return AnalyticsOverview(
        total_leads=total_leads,
        new_leads=new_leads,
        contacted_leads=contacted_leads,
        qualified_leads=qualified_leads,
        converted_leads=converted_leads,
        closed_leads=closed_leads,
        total_projects=total_projects
    )
