
from http import client
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


def web_search(state):
    query = state["topic"]

    print(f"\nSearching the web for: {query}")

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is missing. Add it to your .env file."
        )

    client = TavilyClient(api_key=api_key)

    try:
      response = client.search(
        query=query,
        max_results=5,
        search_depth="basic"
    )
    except Exception as e:
      print(f"Tavily web search failed: {e}")
      return {"web_papers": []}

    papers = []

    for result in response.get("results", []):
        papers.append({
            "title": result.get("title", ""),
            "authors": [],
            "summary": result.get("content", ""),
            "url": result.get("url", ""),
            "source": "web",
            "source_type": "web_result"
        })

    print(f"Found {len(papers)} web results.")

    return {"web_papers": papers}