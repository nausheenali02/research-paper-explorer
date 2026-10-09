import arxiv

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

    return {"papers": papers}