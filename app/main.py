import os
import arxiv

from typing import TypedDict
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# 2. INITIALIZE GEMINI MODEL
# ==========================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


# ==========================================
# 3. DEFINE LANGGRAPH STATE
# ==========================================
class Comparison(BaseModel):
    overall_comparison: str
    similarities: list[str]
    differences: list[str]
    best_approach: str
    
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


# ==========================================
# 4. PYDANTIC STRUCTURED OUTPUT MODELS
# ==========================================

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


# ==========================================
# 5. QUERY ANALYZER NODE
# ==========================================

def query_analyzer(state):

    query = state["query"]

    prompt = f"""
    Analyze this research query:

    {query}

    Identify:
    1. The main research topic
    2. The user's task

    Return the result as structured output.
    """

    structured_model = model.with_structured_output(QueryAnalysis)

    response = structured_model.invoke(prompt)

    print("\n--- Query Analysis ---")
    print("Topic:", response.topic)
    print("Task:", response.task)

    state["topic"] = response.topic
    state["task"] = response.task

    return state


# ==========================================
# 6. RESEARCH PLANNER NODE
# ==========================================

def research_planner(state):

    topic = state["topic"]
    task = state["task"]

    prompt = f"""
    You are a research planning assistant.

    Research topic:
    {topic}

    User's task:
    {task}

    Create a research search plan.

    Decide which sources should be searched.

    Available sources:
    - arxiv
    - web
    - local_vector_db

    Return:
    1. A concise search plan
    2. The sources that should be searched
    """

    structured_model = model.with_structured_output(ResearchPlan)

    response = structured_model.invoke(prompt)

    print("\n--- Research Plan ---")
    print("Plan:", response.search_plan)
    print("Sources:", response.sources)

    state["search_plan"] = response.search_plan
    state["sources"] = response.sources

    return state


# ==========================================
# 7. CONDITIONAL ROUTING
# ==========================================

def route_research(state):

    sources = state["sources"]

    if "arxiv" in sources:
        return "arxiv"

    elif "web" in sources:
        return "web"

    else:
        return "vector_db"


# ==========================================
# 8. ARXIV SEARCH NODE
# ==========================================

def arxiv_search(state):
    
    query = state["topic"]

    print(f"\nSearching ArXiv for recent papers: {query}")

    # Search papers from the last 2 years
    search_query = (
        f'all:"{query}" '
        f'AND submittedDate:[202410080000 TO 202610082359]'
    )

    search = arxiv.Search(
        query=search_query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    client = arxiv.Client()

    papers = []

    for result in client.results(search):

        papers.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "url": result.entry_id
        })

    print(f"Found {len(papers)} recent papers.")

    state["papers"] = papers

    return state


# ==========================================
# 9. PAPER FILTER NODE
# ==========================================

def paper_filter(state):
    
    papers = state["papers"]
    topic = state["topic"]
    task = state["task"]

    relevant_papers = []

    structured_model = model.with_structured_output(PaperRelevance)

    for paper in papers:

        print(f"\nEvaluating: {paper['title']}")

        prompt = f"""
        You are a strict research paper relevance evaluator.

        Research topic:
        {topic}

        User's task:
        {task}

        Paper title:
        {paper["title"]}

        Paper abstract:
        {paper["summary"]}

        Evaluate whether this paper is directly relevant to the research topic.

        A paper should be considered relevant if it specifically focuses on
        one or more of the following:

        - RAG hallucination
        - hallucination detection in RAG
        - hallucination mitigation in RAG
        - RAG faithfulness
        - RAG evaluation related to hallucination
        - retrieval problems that directly cause RAG hallucination

        A paper should NOT be considered relevant merely because
        RAG hallucination appears as one experiment or example.

        Give a relevance score from 0 to 10.

        Score meaning:
        0-3  = Not relevant
        4-6  = Somewhat related
        7-10 = Directly relevant

        A paper is relevant only if its score is 7 or higher.

        Return:
        - relevant: true or false
        - score: 0-10
        - reason: short explanation
        """

        response = structured_model.invoke(prompt)

        print(f"Score: {response.score}")
        print(f"Relevant: {response.relevant}")
        print(f"Reason: {response.reason}")

        if response.relevant and response.score >= 7:
            relevant_papers.append(paper)

    state["relevant_papers"] = relevant_papers

    print(f"\nRelevant papers: {len(relevant_papers)}")

    return state

# ==========================================
# 10. PAPER SUMMARIZER NODE
# ==========================================

def paper_summarizer(state):

    papers = state["relevant_papers"]

    summaries = []

    structured_model = model.with_structured_output(PaperSummary)

    for paper in papers:

        print(f"\nSummarizing: {paper['title']}")

        prompt = f"""
        Analyze this research paper.

        Title:
        {paper["title"]}

        Abstract:
        {paper["summary"]}

        Extract the following information:

        1. What problem does the paper address?
        2. What approach or methodology does it use?
        3. What datasets or benchmarks are used?
        4. What are the main results?
        5. What are the limitations?

        If some information is not available in the abstract,
        clearly say "Not specified in the abstract".

        Return a structured research summary.
        """

        response = structured_model.invoke(prompt)

        summaries.append(response)

    state["summaries"] = summaries

    print(f"\nGenerated summaries: {len(summaries)}")

    return state

def comparison_agent(state):
    
    summaries = state["summaries"]

    print("\nComparing research papers...")

    # Convert structured summaries into readable text
    papers_text = ""

    for i, summary in enumerate(summaries, start=1):

        papers_text += f"""
        PAPER {i}

        Title:
        {summary.title}

        Problem:
        {summary.problem}

        Approach:
        {summary.approach}

        Datasets:
        {summary.datasets}

        Results:
        {summary.results}

        Limitations:
        {summary.limitations}

        --------------------------------
        """

    prompt = f"""
    You are a research comparison agent.

    Compare the following research papers.

    {papers_text}

    Analyze the papers carefully.

    Identify:

    1. The overall comparison between the papers.
    2. Important similarities.
    3. Important differences in their approaches.
    4. Which approach appears strongest for the given research topic,
       and why.

    Do not invent information that is not present in the summaries.

    Return a structured comparison.
    """

    structured_model = model.with_structured_output(Comparison)

    response = structured_model.invoke(prompt)

    state["comparison"] = response

    return state


# ==========================================
# 11. BUILD LANGGRAPH
# ==========================================

builder = StateGraph(State)


# Add nodes

builder.add_node("query_analyzer", query_analyzer)

builder.add_node("research_planner", research_planner)

builder.add_node("arxiv_search", arxiv_search)

builder.add_node("paper_filter", paper_filter)

builder.add_node("paper_summarizer", paper_summarizer)

builder.add_node("comparison_agent", comparison_agent)


# ==========================================
# 12. DEFINE EDGES
# ==========================================

builder.add_edge(
    START,
    "query_analyzer"
)

builder.add_edge(
    "query_analyzer",
    "research_planner"
)


# Conditional routing

builder.add_conditional_edges(
    "research_planner",
    route_research,
    {
        "arxiv": "arxiv_search",
        "web": END,
        "vector_db": END
    }
)


# Remaining workflow

builder.add_edge(
    "arxiv_search",
    "paper_filter"
)

builder.add_edge(
    "paper_filter",
    "paper_summarizer"
)

builder.add_edge(
    "paper_summarizer",
    "comparison_agent"
)

builder.add_edge(
    "comparison_agent",
    END
)


# ==========================================
# 13. COMPILE GRAPH
# ==========================================

graph = builder.compile()


# ==========================================
# 14. RUN THE GRAPH
# ==========================================

result = graph.invoke({
    "query": "Find recent papers on RAG hallucination and compare their approaches."
})


# ==========================================
# 15. DISPLAY PAPERS + SUMMARIES
# ==========================================

print("\n")
print("=" * 80)
print("                 RESEARCH PAPER EXPLORER")
print("=" * 80)

# --------------------------------------------------
# 1. QUERY ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 80)
print("QUERY ANALYSIS")
print("=" * 80)

print(f"\nResearch Topic: {result['topic']}")
print(f"User Task: {result['task']}")


# --------------------------------------------------
# 2. RESEARCH PLAN
# --------------------------------------------------

print("\n" + "=" * 80)
print("RESEARCH PLAN")
print("=" * 80)

print(f"\nPlan: {result['search_plan']}")
print(f"Sources: {', '.join(result['sources'])}")


# --------------------------------------------------
# 3. RELEVANT RESEARCH PAPERS
# --------------------------------------------------

print("\n" + "=" * 80)
print("RELEVANT RESEARCH PAPERS")
print("=" * 80)

for i, paper in enumerate(result["relevant_papers"], start=1):

    print(f"\n{'-' * 80}")
    print(f"PAPER {i}")
    print(f"{'-' * 80}")

    print(f"\nTitle:")
    print(paper["title"])

    print(f"\nAuthors:")
    print(", ".join(paper["authors"]))

    print(f"\nURL:")
    print(paper["url"])

    # Corresponding summary
    summary = result["summaries"][i - 1]

    print("\nPaper Summary:")

    print(f"\nProblem:")
    print(summary.problem)

    print(f"\nApproach:")
    print(summary.approach)

    print(f"\nDatasets / Benchmarks:")
    print(summary.datasets)

    print(f"\nResults:")
    print(summary.results)

    print(f"\nLimitations:")
    print(summary.limitations)


# --------------------------------------------------
# 4. COMPARATIVE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 80)
print("COMPARATIVE ANALYSIS")
print("=" * 80)

comparison = result["comparison"]

print("\nOverall Comparison:")
print(comparison.overall_comparison)


print("\nSimilarities:")

for similarity in comparison.similarities:
    print(f"- {similarity}")


print("\nDifferences:")

for difference in comparison.differences:
    print(f"- {difference}")


print("\nStrongest Approach:")
print(comparison.best_approach)


# --------------------------------------------------
# 5. END
# --------------------------------------------------

print("\n" + "=" * 80)
print("RESEARCH COMPLETE")
print("=" * 80)