from fastapi import FastAPI
from app.models.query import UserQuery

app = FastAPI(title="ORCA Marine AI")


@app.get("/")
def home():
    return {"message": "ORCA Marine AI Backend is running"}


@app.post("/query")
def process_query(request: UserQuery):
    return {
        "message": "Query received",
        "query": request.query,
        "location": request.location,
        "language": request.language,
        "user_type": request.user_type
    }