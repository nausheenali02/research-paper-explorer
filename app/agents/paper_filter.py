
from app.llm import model
from app.models import PaperRelevance


def paper_filter(state):

    papers = state.get("papers", []) + state.get("web_papers", [])
    topic = state["topic"]
    task = state["task"].lower()

    relevant_papers = []

    # Detect whether the user specifically wants academic research
    academic_keywords = [
        "academic paper",
        "academic papers",
        "research paper",
        "research papers",
        "scientific paper",
        "scientific papers",
    ]

    academic_request = any(
        keyword in task for keyword in academic_keywords
    )

    structured_model = model.with_structured_output(PaperRelevance)

    for paper in papers:

        source_type = paper.get("source_type", "unknown")

        # Exclude general web results for academic-paper requests
        if source_type == "web_result" and academic_request:
            print(
                "\nSkipping general web result for an "
                "academic-paper request."
            )
            continue

        print(f"\nEvaluating: {paper['title']}")

        prompt = f"""
        You are a strict research paper relevance evaluator.

        Research topic:
        {topic}

        User's task:
        {task}

        Paper title:
        {paper["title"]}

        Source type:
        {source_type}

        Source URL:
        {paper.get("url", "Not provided")}

        Paper abstract or content:
        {paper.get("summary", "Not provided")}

        RELEVANCE EVALUATION:

        Evaluate relevance based on the research topic and user's task.
        Identify the main concepts, methods, and goals implied by the topic.

        A paper is relevant when its primary contribution directly
        addresses the topic or an important subproblem of it.

        A paper should NOT be considered relevant merely because the
        topic appears as a minor experiment, example, or passing mention.

        Give a relevance score from 0 to 10.

        Score meaning:
        0-3  = Not relevant
        4-6  = Somewhat related
        7-10 = Directly relevant

        A paper is relevant only if its score is 7 or higher.

        SOURCE QUALITY RULES:

        - An ArXiv preprint may count as academic research, but do not
          assume it is peer-reviewed.
        - General web articles, blogs, and product documentation must
          not be presented as academic research papers.
        - When the user requests broader articles or practical
          explanations, relevant web sources may be included.
        - Judge topical relevance separately from source quality.

        Return:
        - relevant: true or false
        - score: 0-10
        - reason: short explanation
        """

        try:
          response = structured_model.invoke(prompt)
        except Exception as e:
          print(f"Paper relevance evaluation failed: {e}")
          continue

        print(f"Score: {response.score}")
        print(f"Relevant: {response.relevant}")
        print(f"Reason: {response.reason}")

        if response.relevant and response.score >= 7:
            relevant_papers.append(paper)

    if not relevant_papers:
        print("\nNo relevant research sources found for this topic.")

    print(f"\nRelevant papers: {len(relevant_papers)}")

    return {"relevant_papers": relevant_papers}