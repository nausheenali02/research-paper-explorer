from app.llm import model
from app.models import PaperRelevance


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

    print(f"\nRelevant papers: {len(relevant_papers)}")

    return {"relevant_papers": relevant_papers}