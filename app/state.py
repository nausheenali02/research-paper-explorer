from typing import TypedDict
from app.models import Comparison


class State(TypedDict):
    query: str
    topic: str
    task: str
    search_plan: str
    sources: list[str]
    papers: list
    relevant_papers: list
    summaries: list
    comparison: Comparison