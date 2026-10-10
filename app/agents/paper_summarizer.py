from app.llm import model
from app.models import PaperSummary


def paper_summarizer(state):
    papers = state["relevant_papers"]

    if not papers:
        print("\nNo relevant sources available to summarize.")
        return {"summaries": []}

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

        try:
         response = structured_model.invoke(prompt)
        except Exception as e:
         print(f"Paper summarization failed: {e}")
         continue
        summaries.append(response)

    print(f"\nGenerated summaries: {len(summaries)}")

    return {"summaries": summaries}