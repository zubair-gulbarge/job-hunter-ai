from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class ApplicationStatus(str, Enum):
    PREPARING = "Preparing"
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    OFFERED = "Offered"
    REJECTED = "Rejected"

class ApplicationModel(BaseModel):
    company_name: str = Field(..., json_schema_extra={"example": "Amazon Web Services"})
    job_title: str = Field(..., json_schema_extra={"example": "Cloud Architect"})
    source: Optional[str] = Field(default="Direct Website", json_schema_extra={"example": "LinkedIn"})
    job_description: str = Field(..., json_schema_extra={"example": "Requires expertise in IAM, RDS, and scalable infrastructure..."})
    status: ApplicationStatus = Field(default=ApplicationStatus.PREPARING)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "company_name": "Amazon Web Services",
                "job_title": "Cloud Architect",
                "source": "LinkedIn",
                "job_description": "Requires expertise in IAM, RDS, and scalable infrastructure...",
                "status": "Preparing"
            }
        }
    )