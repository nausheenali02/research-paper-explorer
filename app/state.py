from typing import Annotated, TypedDict
import operator
from app.models import Comparison


class State(TypedDict):
    query: str
    topic: str
    task: str
    search_plan: str
    sources: list[str]
    papers: Annotated[list, operator.add]
    web_papers: Annotated[list, operator.add]
    relevant_papers: list
    summaries: list
    comparison: Comparison