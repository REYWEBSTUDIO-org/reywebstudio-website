from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# --- AUTH SCHEMAS ---
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- LEAD SCHEMAS ---
class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=1)

class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    message: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(new|contacted|qualified|converted|closed)$")

class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- PROJECT SCHEMAS ---
class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1)
    image_url: str = Field(..., min_length=1, max_length=500)
    live_url: Optional[str] = Field(None, max_length=500)
    category: str = Field("Web Design", max_length=50)
    featured: bool = False

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    live_url: Optional[str] = None
    category: Optional[str] = None
    featured: Optional[bool] = None

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: str
    live_url: Optional[str] = None
    category: str
    featured: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- ANALYTICS SCHEMAS ---
class AnalyticsOverview(BaseModel):
    total_leads: int
    new_leads: int
    contacted_leads: int
    qualified_leads: int
    converted_leads: int
    closed_leads: int
    total_projects: int
