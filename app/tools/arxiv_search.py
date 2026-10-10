import arxiv
from datetime import datetime, timedelta, timezone
def arxiv_search(state):

    query = state["topic"]

    print(f"\nSearching ArXiv for recent papers: {query}")
    
    today = datetime.now(timezone.utc).date() 
    two_years_ago = today - timedelta(days=730)
    
    start_date = two_years_ago.strftime("%Y%m%d") + "0000" 
    end_date = today.strftime("%Y%m%d") + "2359"
    # Search papers from the last 2 years
    search_query = (
        f'all:"{query}" '
        f'AND submittedDate:[{start_date} TO {end_date}]'
    )

    search = arxiv.Search(
        query=search_query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    client = arxiv.Client()

    papers = []

    try:
     for result in client.results(search):
        papers.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "url": result.entry_id,
            "source_type": "arxiv_preprint",
        })

    except Exception as e:
      print(f"ArXiv search failed: {e}")
        
    if not papers:
        print("No recent papers found on ArXiv for this topic.")

    print(f"Found {len(papers)} recent papers.")

    return {"papers": papers}