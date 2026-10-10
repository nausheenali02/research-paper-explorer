from app.llm import model
from app.models import ResearchPlan


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

    
    Available sources (choose only from this list):
    - arxiv
    - web

   Rules:
   - Select only sources listed above.
   - Do not return local_vector_db or any other unsupported source.
   - Return source names exactly as written.

    

    Return:
    1. A concise search plan
    2. The sources that should be searched
    """

    structured_model = model.with_structured_output(ResearchPlan)

    try:
      response = structured_model.invoke(prompt)
    except Exception as e:
      print(f"Research planning failed: {e}")
      raise

    print("\n--- Research Plan ---")
    print("Plan:", response.search_plan)
    print("Sources:", response.sources)

    return {
        "search_plan": response.search_plan,
        "sources": response.sources
    }