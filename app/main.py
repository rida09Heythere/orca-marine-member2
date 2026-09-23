from fastapi import FastAPI
from app.models.query import UserQuery
from app.models.response import ORCAResponse
from app.services.llm import ask_llm
from app.agents.safety_agent import safety_agent

app = FastAPI(title="ORCA Marine AI")


@app.get("/")
def home():
    return {"message": "ORCA Marine AI Backend is running"}


@app.post("/query", response_model=ORCAResponse)
def process_query(request: UserQuery):

    safety_result = safety_agent(
        request.query,
        request.location
    )

    tool_result = safety_result["result"]

    evidence = None

    if tool_result:
        tool_data = tool_result.get("data") or {}

        evidence = {
        "source": "ORCA Geofence Safety Tool",
        "tool": safety_result["tool_used"],
        "status": tool_result.get("status"),
        "latitude": tool_data.get("latitude"),
        "longitude": tool_data.get("longitude"),
        "distance_to_boundary_m": tool_data.get(
        "distance_to_boundary_m"
         ),
        "message": tool_result.get("message")
        }

    answer = ask_llm(
        request.query,
        tool_result
    )

    return {
        "query": request.query,
        "location": request.location,
        "language": request.language,
        "user_type": request.user_type,
        "agent": {
            "name": "Safety Agent",
            "tool_used": safety_result["tool_used"]
        },
        "answer": answer,
        "evidence": evidence
    }
