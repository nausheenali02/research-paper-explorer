from langgraph.graph import StateGraph, START, END
from app.state import State
from app.tools.arxiv_search import arxiv_search
from app.tools.web_search import web_search

from app.agents.query_analyzer import query_analyzer
from app.agents.research_planner import research_planner
from app.tools.arxiv_search import arxiv_search
from app.agents.paper_filter import paper_filter
from app.agents.paper_summarizer import paper_summarizer
from app.agents.comparison_agent import comparison_agent

def search_sources(state: State):
    sources = state.get("sources", [])
    results = {
        "papers": [],
        "web_papers": []
    }

    if "arxiv" in sources:
        results.update(arxiv_search(state))

    if "web" in sources:
        results.update(web_search(state))

    if not sources:
        results.update(arxiv_search(state))

    return results

def build_graph():

    builder = StateGraph(State)

    # Register nodes
    builder.add_node("query_analyzer", query_analyzer)
    builder.add_node("research_planner", research_planner)
    builder.add_node("search_sources", search_sources)
    builder.add_node("paper_filter", paper_filter)
    builder.add_node("paper_summarizer", paper_summarizer)
    builder.add_node("comparison_agent", comparison_agent)

    # Initial workflow
    builder.add_edge(START, "query_analyzer")
    builder.add_edge("query_analyzer", "research_planner")

    # Conditional routing
    builder.add_edge("research_planner", "search_sources")

    # Remaining workflow
    builder.add_edge("search_sources", "paper_filter")
    builder.add_edge("paper_filter", "paper_summarizer")
    builder.add_edge("paper_summarizer", "comparison_agent")
    builder.add_edge("comparison_agent", END)

    return builder.compile()