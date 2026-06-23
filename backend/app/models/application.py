from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Define strict statuses for the frontend Kanban board
class ApplicationStatus(str, Enum):
    PREPARING = "Preparing"
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFERED = "Offered"
    REJECTED = "Rejected"

class ApplicationModel(BaseModel):
    company_name: str = Field(..., example="Amazon Web Services")
    job_title: str = Field(..., example="Cloud Architect")
    job_description: str = Field(..., example="Requires expertise in IAM, RDS, and scalable infrastructure...")
    tailored_resume_text: Optional[str] = Field(None, description="The AI-generated resume used for this job")
    status: ApplicationStatus = Field(default=ApplicationStatus.PREPARING)
    applied_date: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Tech Corp",
                "job_title": "Platform Engineer",
                "job_description": "Paste the full JD here...",
                "status": "Preparing"
            }
        }