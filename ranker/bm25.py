from typing import List, Dict, Tuple
import math


class BM25:
    @staticmethod
    def compute(postings: Dict[str, List[Tuple[int, int]]], df_map: Dict[str, int], N: int) -> Dict[int, Dict[str, float]]:
        """
        Compute BM25 scores for the provided postings and df map.

        Parameters:
        - postings: dict mapping term -> list of (doc_id, tf)
        - df_map: dict mapping term -> document frequency (int)
        - N: total number of documents (int)

        Returns:
        - dict mapping doc_id -> { term: bm25_score, ... }
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
            
            # BM25 parameters (b=0 assuming no length normalization info available)
            k1 = 1.5

            for doc_id, tf in posting_list:
                try:
                    tf_val = float(tf)
                except Exception:
                    try:
                        tf_val = float(int(tf))
                    except Exception:
                        tf_val = 0.0
                
                # BM25 computation with b=0: (tf * (k1 + 1)) / (tf + k1)
                numerator = tf_val * (k1 + 1)
                denominator = tf_val + k1
                bm25_tf = numerator / denominator
                
                # Final score for the term in this doc
                score = bm25_tf * idf
                
                if doc_id not in result:
                    result[doc_id] = {}
                result[doc_id][term] = score

        return result

    @staticmethod
    def compute_query_weights(tf_counts: Dict[str, int], df_map: Dict[str, int], N: int) -> Dict[str, float]:
        """
        Compute query weights. With BM25 in the doc vector, we just need frequency here.
        """
        out: Dict[str, float] = {}
        # N is unused for query weights in this BM25 implementation logic
        
        for term, tf in tf_counts.items():
            # We use raw frequency for the query vector (or 1 / binary)
            # The IDF is already collected in the document scoring phase.
            out[term] = float(tf)
        return out


