from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- NEW IMPORT
# ... (your other imports stay the same)
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
# --- NEW: CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allows your Vite React app to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

class TailorRequest(BaseModel):
    master_resume: str
    job_description: str

@app.post("/api/tailor-resume", response_class=FileResponse)
async def generate_tailored_resume(request: TailorRequest):
    try:
        # 1. Fetch the actual Master Profile from MongoDB
        profile = await profiles_collection.find_one({}, {"_id": 0})
        if not profile:
            raise HTTPException(status_code=400, detail="Master profile not found. Please save your profile first.")

        # 2. Format the experience data cleanly for the HTML template
        experience_html = ""
        if "experience" in profile and profile["experience"]:
            for exp in profile["experience"]:
                experience_html += f"""
                <div class="item-header">
                    <span>{exp.get('company', '')}</span>
                    <span>{exp.get('duration', '')}</span>
                </div>
                <div class="item-subheader">
                    <span>{exp.get('role', '')}</span>
                </div>
                <ul><li>{exp.get('description', '')}</li></ul>
                """

        # 3. Format the projects data
        projects_html = ""
        if "projects" in profile and profile["projects"]:
            for proj in profile["projects"]:
                projects_html += f"""
                <div class="item-header">
                    <span>{proj.get('title', '')}</span>
                    <span></span>
                </div>
                <div class="item-subheader">
                    <span>Technologies: {proj.get('technologies', '')}</span>
                </div>
                <ul><li>{proj.get('description', '')}</li></ul>
                """

        # 4. Format the skills array back into a readable string
        skills_string = ", ".join(profile.get("skills", []))

        # 5. Build the data package for the PDF Template (Harvard Style)
        resume_data = {
            "name": profile.get("name", ""),
            "email": profile.get("email", ""),
            "phone": profile.get("phone", ""),
            "portfolio_url": "github.com/zubairgulbarge",
            "summary": profile.get("summary", ""),
            "skills": skills_string,
            "experience_html": experience_html,
            "projects_html": projects_html,
            "education": profile.get("academics", [{}])[0] if profile.get("academics") else None
        }
        
        # 6. Generate the PDF using the template
        pdf_file_path = generate_pdf_from_data(resume_data)
        
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
    
@app.delete("/api/applications/{app_id}")
async def delete_application(app_id: str):
    try:
        result = await applications_collection.delete_one({"_id": ObjectId(app_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Application not found.")
        return {"status": "success", "message": "Application deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))