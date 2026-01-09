class PrecisionAt_10:
    def __init__(self):
        pass

    def precision_at_10(self, ranked_docs: list[int], relevant_docs: list[int]) -> float:
        top10 = ranked_docs[:10]
        if not top10:
            return 0.0

        relevant_set = set(relevant_docs)
        relevant_in_top10 = sum(
            1 for doc_id in top10 if doc_id in relevant_set
        )
        return relevant_in_top10 / 10
