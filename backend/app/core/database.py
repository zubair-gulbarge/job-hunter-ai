import os
from motor.motor_asyncio import AsyncIOMotorClient

# Fallback to local docker credentials if env variables aren't set yet
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://admin:secretpassword@localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)

# Define the database name
database = client.job_hunter_ai

# Database collections (think of these as tables)
applications_collection = database.get_collection("applications")
profiles_collection = database.get_collection("profiles")