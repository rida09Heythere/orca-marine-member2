from fastapi import FastAPI

from app.models.query import UserQuery
from app.models.response import ORCAResponse
from app.services.llm import ask_llm

from app.agents.safety_agent import safety_agent
from app.agents.result_summarizer import summarize_results


app = FastAPI(title="ORCA Marine AI")


@app.get("/")
def home():
    return {
        "message": "ORCA Marine AI Backend is running"
    }


@app.post("/query", response_model=ORCAResponse)
def process_query(request: UserQuery):

    # 1. Run the Safety Agent
    safety_result = safety_agent(
        request.query,
        request.location
    )

    # 2. Get the tool results
    tool_results = safety_result.get("results", [])

    # 3. Summarize the results
    summary = summarize_results(tool_results)

    # 4. Send all tool results to the LLM
    answer = ask_llm(
        request.query,
        summary
    )

    # 5. Convert tool results into evidence
    evidence = []

    for result in tool_results:
        evidence.append({
            "source": result.get("source"),
            "tool": result.get("tool"),
            "status": result.get("status"),
            "data": result.get("data"),
            "message": result.get("message")
        })

    # 6. Return structured ORCA response
    
        return ORCAResponse(
    query=request.query,
    location=request.location,
    language=request.language,
    user_type=request.user_type,

    agent={
        "name": safety_result.get(
            "agent",
            "Safety Agent"
        ),
        "tools_used": safety_result.get(
            "tools_selected",
            []
        )
    },

    answer=answer,

    safety=safety_result.get("safety"),

    evidence=evidence
)