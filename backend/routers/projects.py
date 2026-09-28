from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Project, AdminUser
from backend.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.security import get_current_admin

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectResponse])
def get_projects(
    category: Optional[str] = None,
    featured_only: Optional[bool] = Query(False, alias="featured"),
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    if category:
        query = query.filter(Project.category == category)
    if featured_only:
        query = query.filter(Project.featured == True)
    projects = query.order_by(Project.created_at.desc()).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    new_project = Project(
        title=payload.title,
        description=payload.description,
        image_url=payload.image_url,
        live_url=payload.live_url,
        category=payload.category,
        featured=payload.featured
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if payload.title is not None:
        project.title = payload.title
    if payload.description is not None:
        project.description = payload.description
    if payload.image_url is not None:
        project.image_url = payload.image_url
    if payload.live_url is not None:
        project.live_url = payload.live_url
    if payload.category is not None:
        project.category = payload.category
    if payload.featured is not None:
        project.featured = payload.featured

    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return None
