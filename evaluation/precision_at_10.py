class PrecisionAt_10:
    def __init__(self, gold_standard):
        self.gold = gold_standard

    def precision_at_10(self, query: str, ranked_docs: list[str]) -> float:
        top10 = ranked_docs[:10]
        relevant = self.gold.get_relevant_docs(query)

        if not top10:
            return 0.0

        relevant_in_top10 = sum(
            1 for doc_id in top10 if doc_id in relevant
        )
        return relevant_in_top10 / 10


    # def average_precision_at_10()
