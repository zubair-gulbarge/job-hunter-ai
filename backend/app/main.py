from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.llm_service import tailor_resume_content
from app.models.profile import ProfileModel
from app.core.database import profiles_collection
# Add this to your existing imports
from bson import ObjectId
from app.models.application import ApplicationModel, ApplicationStatus
from app.core.database import applications_collection
from fastapi.responses import FileResponse
from app.services.pdf_service import generate_pdf_from_data

app = FastAPI(title="Job Hunter AI")

class TailorRequest(BaseModel):
    master_resume: str
    job_description: str

# @app.post("/api/tailor-resume")
# async def generate_tailored_resume(request: TailorRequest):
#     try:
#         tailored_text = tailor_resume_content(
#             master_resume=request.master_resume,
#             job_description=request.job_description
#         )
#         return {"status": "success", "tailored_resume": tailored_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/tailor-resume", response_class=FileResponse)
async def generate_tailored_resume(request: TailorRequest):
    try:
        # 1. Ask the AI to tailor the text based on the Master Resume and JD
        tailored_text = tailor_resume_content(
            master_resume=request.master_resume,
            job_description=request.job_description
        )
        
        # 2. Package the data for the template (In a full implementation, 
        # the AI should return structured JSON so you can map these fields perfectly)
        resume_data = {
            "name": "Zubair Gulbarge",
            "email": "zubairgulbarge@gmail.com",
            "phone": "+91 9833698785",
            "portfolio_url": "zubairlearntech.com",
            "summary": "Cloud and DevOps professional tailored for this specific role.",
            "skills": "AWS (IAM, RDS, S3), Python, Docker, FastAPI",
            "experience_html": f"<div>{tailored_text}</div>"
        }
        
        # 3. Generate the PDF
        pdf_file_path = generate_pdf_from_data(resume_data)
        
        # 4. Return the file as a downloadable attachment
        return FileResponse(
            path=pdf_file_path, 
            filename="Zubair_Tailored_Resume.pdf", 
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NEW: Master Profile Endpoints ---

@app.post("/api/profile", status_code=201)
async def save_or_update_profile(profile: ProfileModel):
    try:
        # Convert Pydantic model to a standard dictionary for MongoDB
        profile_dict = profile.model_dump()
        
        # We will use a single "master" profile entry for now. 
        #upsert=True means: update if exists, insert if it doesn't.
        await profiles_collection.update_one(
            {"email": profile.email}, 
            {"$set": profile_dict}, 
            upsert=True
        )
        return {"status": "success", "message": "Master profile saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/profile")
async def get_profile():
    # Fetch the first profile found in the database
    profile = await profiles_collection.find_one({}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="No profile found. Please create one first.")
    return profile

# --- NEW: Application Tracking Endpoints ---

@app.post("/api/applications", status_code=201)
async def create_application(application: ApplicationModel):
    try:
        app_dict = application.model_dump()
        result = await applications_collection.insert_one(app_dict)
        return {
            "status": "success", 
            "message": "Application tracked.", 
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications")
async def get_all_applications():
    try:
        applications = []
        # Fetch all records, sort by newest first
        cursor = applications_collection.find().sort("applied_date", -1)
        async for document in cursor:
            # Convert MongoDB's ObjectId to a standard string for the frontend
            document["_id"] = str(document["_id"])
            applications.append(document)
        return applications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/applications/{app_id}/status")
async def update_application_status(app_id: str, new_status: ApplicationStatus):
    try:
        result = await applications_collection.update_one(
            {"_id": ObjectId(app_id)},
            {"$set": {"status": new_status}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Application not found or status unchanged.")
        return {"status": "success", "message": f"Status updated to {new_status}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))