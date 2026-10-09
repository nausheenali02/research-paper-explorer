from pydantic import BaseModel

class Comparison(BaseModel):
    overall_comparison: str
    similarities: list[str]
    differences: list[str]
    best_approach: str


class QueryAnalysis(BaseModel):
    topic: str
    task: str


class ResearchPlan(BaseModel):
    search_plan: str
    sources: list[str]


class PaperSummary(BaseModel):
    title: str
    problem: str
    approach: str
    datasets: str
    results: str
    limitations: str


class PaperRelevance(BaseModel):
    relevant: bool
    score: int
    reason: str