from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectSchema(BaseModel):
    title: str = Field(..., example="CloudBox")
    description: str = Field(..., example="Secure multi-user file management application using Python and Flask.")
    technologies: List[str] = Field(..., example=["Python", "Flask", "Docker", "MongoDB"])

class AcademicSchema(BaseModel):
    degree: str = Field(..., example="Bachelor of Technology in Computer Science")
    institution: str = Field(..., example="University Name")
    graduation_year: str = Field(..., example="2025")

class ProfileModel(BaseModel):
    name: str = Field(..., example="Zubair")
    email: str = Field(..., example="zubair@example.com")
    phone: Optional[str] = Field(None, example="+91 9876543210")
    skills: List[str] = Field(..., example=["Python", "AWS", "Docker", "Terraform"])
    academics: List[AcademicSchema]
    projects: List[ProjectSchema]

    class Config:
        json_schema_extra = {
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