from typing import Dict
import math


class ScoreAccumulator:
    @staticmethod
    def aggregate_scores(query_w: Dict[str, float], doc_scores: Dict[int, Dict[str, float]]) -> Dict[int, float]:
        """
        Aggregate scores (dot product) between query weights and document partial scores.
        
        This assumes doc_scores already contains the relevant metric (e.g. BM25).
        It simply sums them up based on query term weights.

        Parameters:
        - query_w: dict term -> weight (e.g. raw count)
        - doc_scores: dict doc_id -> { term -> score }

        Returns:
        - dict doc_id -> total score (float)
        """
        if not query_w or not doc_scores:
            return {doc_id: 0.0 for doc_id in doc_scores} if doc_scores else {}

        scores: Dict[int, float] = {}

        for doc_id, dvec in doc_scores.items():
            # compute dot product only over overlapping terms
            dot = 0.0
            for term, qw in query_w.items():
                ds = dvec.get(term)
                if ds is None:
                    continue
                try:
                    dot += float(qw) * float(ds)
                except Exception:
                    continue

            scores[doc_id] = dot

        return scores
 