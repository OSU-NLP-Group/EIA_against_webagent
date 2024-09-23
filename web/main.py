from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection settings
try:
    db_client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = db_client.mlb
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    # Handle connection error appropriately

class User(BaseModel):
    email: str

@app.post("/submit_data")
async def submit_data(user: User):
    try:
        print(user.dict())
        await db.lzy_collection.insert_one(user.dict())
        return {"message": "Form data received and saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        # Attempt to fetch data from MongoDB
        await db.command("ping")
        return {"status": "MongoDB is connected and responsive"}
    except Exception as e:
        return {"status": "MongoDB connection failed", "error": str(e)}

app.mount("/webpages", StaticFiles(directory="../data/webpages_filtered"), name="webpages")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


