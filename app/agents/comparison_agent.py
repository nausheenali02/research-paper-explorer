from app.llm import model
from app.models import Comparison


def comparison_agent(state):
    
    summaries = state["summaries"]

    if not summaries:
        print("\nNo summaries available for comparison.")
        return {
            "comparison": Comparison(
                overall_comparison="No relevant sources were found to compare.",
                similarities=[],
                differences=[],
                best_approach="Not enough information to determine."
            )
        }
    if len(summaries) == 1:
        print("\nOnly one relevant source found. Skipping comparison.")
        return {
          "comparison": Comparison(
            overall_comparison="Only one relevant source was found. A cross-paper comparison is not possible.",
            similarities=[],
            differences=[],
            best_approach="Not enough sources to determine."
        )
    }

    print("\nComparing research papers...")

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

    try:
      response = structured_model.invoke(prompt)
    except Exception as e:
      print(f"Paper comparison failed: {e}")
      raise

    return {"comparison": response}