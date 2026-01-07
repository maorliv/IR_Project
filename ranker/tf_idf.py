from typing import List, Dict, Tuple
import math


class TfIdf:
    @staticmethod
    def compute(postings: Dict[str, List[Tuple[int, int]]], df_map: Dict[str, int], N: int) -> Dict[int, Dict[str, float]]:
        """
        Compute TF-IDF for the provided postings and df map.

        Parameters:
        - postings: dict mapping term -> list of (doc_id, tf)
        - df_map: dict mapping term -> document frequency (int)
        - N: total number of documents (int)

        Returns:
        - dict mapping doc_id -> { term: tfidf, ... }
        """
        if N <= 0:
            return {}

        result: Dict[int, Dict[str, float]] = {}

        for term, posting_list in (postings or {}).items():
            if not posting_list:
                continue
            df = int(df_map.get(term, len(posting_list) if posting_list is not None else 0))
            if df <= 0:
                idf = 0.0
            else:
                # standard idf = log2(N / df)
                idf = math.log2(N / df) if df > 0 else 0.0

            for doc_id, tf in posting_list:
                try:
                    tf_val = float(tf)
                except Exception:
                    try:
                        tf_val = float(int(tf))
                    except Exception:
                        tf_val = 0.0
                tfidf = tf_val * idf
                if doc_id not in result:
                    result[doc_id] = {}
                result[doc_id][term] = tfidf

        return result

    @staticmethod
    def compute_query_tfidf(tf_counts: Dict[str, int], df_map: Dict[str, int], N: int) -> Dict[str, float]:
        """
        Compute TF-IDF for a query represented by term counts.

        Parameters:
        - tf_counts: dict term -> raw count in query
        - df_map: dict term -> document frequency
        - N: total number of documents

        Returns:
        - dict term -> tfidf (float)
        """
        import math
        out: Dict[str, float] = {}
        if N <= 0:
            for t in tf_counts:
                out[t] = 0.0
            return out

        for term, tf in tf_counts.items():
            df = int(df_map.get(term, 0))
            if df <= 0:
                idf = 0.0
            else:
                idf = math.log2(N / df)
            out[term] = float(tf) * idf
        return out


