from langgraph.graph import StateGraph, START, END

from app.state import State

from app.agents.query_analyzer import query_analyzer
from app.agents.research_planner import research_planner
from app.tools.arxiv_search import arxiv_search
from app.agents.paper_filter import paper_filter
from app.agents.paper_summarizer import paper_summarizer
from app.agents.comparison_agent import comparison_agent


def route_research(state: State):

    sources = state["sources"]

    if "arxiv" in sources:
        return "arxiv"

    elif "web" in sources:
        return "web"

    else:
        return "vector_db"


def build_graph():

    builder = StateGraph(State)

    # Register nodes
    builder.add_node("query_analyzer", query_analyzer)
    builder.add_node("research_planner", research_planner)
    builder.add_node("arxiv_search", arxiv_search)
    builder.add_node("paper_filter", paper_filter)
    builder.add_node("paper_summarizer", paper_summarizer)
    builder.add_node("comparison_agent", comparison_agent)

    # Initial workflow
    builder.add_edge(START, "query_analyzer")
    builder.add_edge("query_analyzer", "research_planner")

    # Conditional routing
    builder.add_conditional_edges(
        "research_planner",
        route_research,
        {
            "arxiv": "arxiv_search",
            "web": END,
            "vector_db": END,
        },
    )

    # Remaining workflow
    builder.add_edge("arxiv_search", "paper_filter")
    builder.add_edge("paper_filter", "paper_summarizer")
    builder.add_edge("paper_summarizer", "comparison_agent")
    builder.add_edge("comparison_agent", END)

    return builder.compile()