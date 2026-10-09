from app.llm import model
from app.models import QueryAnalysis


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

    return {
        "topic": response.topic,
        "task": response.task
    }