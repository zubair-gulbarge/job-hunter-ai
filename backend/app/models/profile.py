from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class ProjectSchema(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "CloudBox"})
    description: str = Field(..., json_schema_extra={"example": "Secure multi-user file management application using Python and Flask."})
    technologies: List[str] = Field(..., json_schema_extra={"example": ["Python", "Flask", "Docker", "MongoDB"]})

class AcademicSchema(BaseModel):
    degree: str = Field(..., json_schema_extra={"example": "Bachelor of Technology in Computer Science"})
    institution: str = Field(..., json_schema_extra={"example": "University Name"})
    graduation_year: str = Field(..., json_schema_extra={"example": "2025"})

class ProfileModel(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Zubair"})
    email: str = Field(..., json_schema_extra={"example": "zubair@example.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+91 9876543210"})
    skills: List[str] = Field(..., json_schema_extra={"example": ["Python", "AWS", "Docker", "Terraform"]})
    academics: List[AcademicSchema] = Field(default_factory=list)
    projects: List[ProjectSchema] = Field(default_factory=list)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Zubair",
                "email": "zubair@example.com",
                "phone": "+91 9876543210",
                "skills": ["Python", "AWS", "Docker", "FastAPI"],
                "academics": [
                    {
                        "degree": "B.Tech in Computer Science",
                        "institution": "State University",
                        "graduation_year": "2025"
                    }
                ],
                "projects": [
                    {
                        "title": "CloudBox",
                        "description": "Secure multi-user file management application using Python and Flask.",
                        "technologies": ["Python", "Flask", "MongoDB", "Docker"]
                    }
                ]
            }
        }
    )