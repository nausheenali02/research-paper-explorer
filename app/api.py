
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph.workflow import build_graph

app = FastAPI(title="Research Paper Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "Research Paper Explorer API is running!"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/research")
def research(request: ResearchRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Please enter a research query."
        )

    try:
        graph = build_graph()

        result = graph.invoke({
            "query": query
        })

        return {
            "query": query,
            "topic": result["topic"],
            "task": result["task"],
            "search_plan": result["search_plan"],
            "sources": result["sources"],
            "papers": [
                {
                    "title": paper.get("title", "Untitled"),
                    "source_type": paper.get("source_type", "unknown"),
                    "authors": paper.get("authors", []),
                    "url": paper.get("url", ""),
                }
                for paper in result.get("relevant_papers", [])
            ],
            "summaries": [
                summary.model_dump()
                for summary in result.get("summaries", [])
            ],
            "comparison": result["comparison"].model_dump(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Research workflow failed: {str(exc)}"
        ) from exc
