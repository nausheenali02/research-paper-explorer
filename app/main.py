from app.graph.workflow import build_graph

def main():

    graph = build_graph()

    result = graph.invoke({
        "query": "Find recent papers on RAG hallucination and compare their approaches."
    })

    print("\n")
    print("=" * 80)
    print("                 RESEARCH PAPER EXPLORER")
    print("=" * 80)

    # Query Analysis
    print("\n" + "=" * 80)
    print("QUERY ANALYSIS")
    print("=" * 80)

    print(f"\nResearch Topic: {result['topic']}")
    print(f"User Task: {result['task']}")

    # Research Plan
    print("\n" + "=" * 80)
    print("RESEARCH PLAN")
    print("=" * 80)

    print(f"\nPlan: {result['search_plan']}")
    print(f"Sources: {', '.join(result['sources'])}")

    # Relevant Papers and Summaries
    print("\n" + "=" * 80)
    print("RELEVANT RESEARCH PAPERS")
    print("=" * 80)

    for i, paper in enumerate(result["relevant_papers"], start=1):

        print(f"\n{'-' * 80}")
        print(f"PAPER {i}")
        print(f"{'-' * 80}")

        print(f"\nTitle:\n{paper['title']}")
        print(f"\nAuthors:\n{', '.join(paper['authors'])}")
        print(f"\nURL:\n{paper['url']}")

        summary = result["summaries"][i - 1]

        print(f"\nProblem:\n{summary.problem}")
        print(f"\nApproach:\n{summary.approach}")
        print(f"\nDatasets / Benchmarks:\n{summary.datasets}")
        print(f"\nResults:\n{summary.results}")
        print(f"\nLimitations:\n{summary.limitations}")

    # Comparative Analysis
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

    print("\n" + "=" * 80)
    print("RESEARCH COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()