from typing import Dict
import math


class CosineSimilarity:
    @staticmethod
    def compute(query_vec: Dict[str, float], doc_vecs: Dict[int, Dict[str, float]]) -> Dict[int, float]:
        """
        Compute cosine similarity between a query vector and multiple document vectors.

        Parameters:
        - query_vec: dict term -> tfidf (query)
        - doc_vecs: dict doc_id -> { term -> tfidf }

        Returns:
        - dict doc_id -> cosine similarity (float)
        """
        if not query_vec or not doc_vecs:
            return {doc_id: 0.0 for doc_id in doc_vecs} if doc_vecs else {}

        # precompute query norm
        q_norm_sq = 0.0
        for v in query_vec.values():
            try:
                q_norm_sq += float(v) * float(v)
            except Exception:
                continue
        q_norm = math.sqrt(q_norm_sq)

        scores: Dict[int, float] = {}

        for doc_id, dvec in doc_vecs.items():
            # compute dot product only over overlapping terms
            dot = 0.0
            for term, qv in query_vec.items():
                dv = dvec.get(term)
                if dv is None:
                    continue
                try:
                    dot += float(qv) * float(dv)
                except Exception:
                    continue

            # compute document norm
            d_norm_sq = 0.0
            for v in dvec.values():
                try:
                    d_norm_sq += float(v) * float(v)
                except Exception:
                    continue
            d_norm = math.sqrt(d_norm_sq)

            if q_norm == 0.0 or d_norm == 0.0:
                scores[doc_id] = 0.0
            else:
                scores[doc_id] = dot / (q_norm * d_norm)

        return scores
 