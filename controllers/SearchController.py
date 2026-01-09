from typing import List, Dict, Tuple

from data_provider.data_provider import DataProvider
from text_processor.query_tokenize import QueryTokenize
from ranker.bm25 import BM25
from ranker.score_accumulator import ScoreAccumulator

class SearchController:
    def __init__(self, base_dir: str, query: str = "", weight_text: float = 0.8, weight_pagerank: float = 0.2):
        # `query` parameter kept for backwards compatibility with tests
        # weights are configurable and stored on the controller; no hardcoded
        # values are used inside ranking methods.
        self.data_provider = DataProvider(base_dir=base_dir)
        self.query_tk = QueryTokenize()
        self.ranker = BM25()
        self.weight_text = float(weight_text)
        self.weight_pagerank = float(weight_pagerank)
        
        # backward compatibility aliases if needed by tests outside (though tests inject controller usually)
        self.weight_cosine = self.weight_text


    def query_to_tokens(self, query: str) -> List[str]:
        return self.query_tk.tokenize(query)

    def tokens_df(self, tokens: List[str]) -> Dict[str, int]:
        return self.data_provider.get_df(tokens)

    def tokens_postings(self, tokens: List[str]):
        return self.data_provider.get_posting_list(tokens)

    def corpus_size(self) -> int:
        return self.data_provider.corpus_size()

    def compute_doc_scores(self, query: str):
        """Tokenize query, fetch posting lists, df and N, compute BM25 scores.

        Returns: dict mapping doc_id -> {term: score}
        """
        tokens = self.query_to_tokens(query)
        if not tokens:
            return {}
        postings = self.tokens_postings(tokens)
        df_map = self.tokens_df(tokens)
        N = self.corpus_size()
        return self.ranker.compute(postings=postings, df_map=df_map, N=N)

    def get_query_term_weights(self, query: str) -> Dict[str, float]:
        """
        Compute weights for the query terms (raw frequency).

        Parameters:
        - tokens: tokenized query (after stopword removal)

        Returns:
        - dict mapping term -> weight
        """
        tokens = self.query_to_tokens(query)

        if not tokens:
            return {}
        from collections import Counter
        
        tf_counts = Counter(tokens)
        terms = list(tf_counts.keys())
        df_map = self.tokens_df(terms)
        N = self.corpus_size()

        # delegate query weight calculation to BM25 utility
        return self.ranker.compute_query_weights(tf_counts=tf_counts, df_map=df_map, N=N)

    def compute_ranking_scores(self, query: str) -> Dict[int, float]:
        """
        Compute final ranking scores (Text + PageRank).
        Returns a mapping doc_id -> score.
        """
        # compute text-only scores (BM25 aggregation)
        text_scores = self._compute_text_scores(query)
        if not text_scores:
            return {}

        # fetch pagerank for the candidate set
        doc_ids = list(text_scores.keys())
        pr_scores = self._get_pagerank_scores(doc_ids)

        # combine
        combined = self._combine_scores(text_scores, pr_scores)
        return combined

    def _compute_text_scores(self, query: str) -> Dict[int, float]:
        """Compute text similarity scores between query and documents (BM25).

        Returns dict doc_id -> score (float).
        """
        doc_scores = self.compute_doc_scores(query)
        query_w = self.get_query_term_weights(query)
        if not query_w or not doc_scores:
            return {}
        return ScoreAccumulator.aggregate_scores(query_w=query_w, doc_scores=doc_scores)

    def _get_pagerank_scores(self, doc_ids: List[int]) -> Dict[int, float]:
        """Fetch PageRank scores for the given doc ids. Always reads from disk/provider.

        Returns dict doc_id -> pagerank (float). Missing ids map to 0.0.
        """
        if not doc_ids:
            return {}
        try:
            pr = self.data_provider.get_pagerank(doc_ids)
            # ensure keys are ints and values are floats
            return {int(d): float(v) for d, v in pr.items()}
        except Exception:
            # on failure, return zeros for all docs
            return {int(d): 0.0 for d in doc_ids}

    def _combine_scores(self, text_scores: Dict[int, float], pr_scores: Dict[int, float]) -> Dict[int, float]:
        """Combine text(BM25) and pagerank scores using controller weights.

        No hardcoded weights here; uses `self.weight_text` and
        `self.weight_pagerank` provided at construction.
        """
        if not text_scores:
            return {}

        import math

        # 1. Normalize BM25/Text scores (Min-Max)
        # ScoreAccumulator returns raw BM25 summation scores
        c_vals = list(text_scores.values())
        c_max = max(c_vals)
        c_min = min(c_vals)
        c_diff = c_max - c_min
        if c_diff == 0:
            c_diff = 1.0

        # 2. Log-scale PageRank and normalize (Min-Max)
        # PageRank is power-law distributed, so log-scale is essential.
        epsilon = 1e-8
        log_pr_vals = {}
        # compute logs for all relevant docs
        for did in text_scores:
            val = pr_scores.get(did, 0.0)
            # handle zero or extremely small PR
            log_pr_vals[did] = math.log10(val if val > epsilon else epsilon)
            
        lp_vals = list(log_pr_vals.values())
        lp_max = max(lp_vals)
        lp_min = min(lp_vals)
        lp_diff = lp_max - lp_min
        if lp_diff == 0:
            lp_diff = 1.0

        combined: Dict[int, float] = {}
        for did, raw_score in text_scores.items():
            # Normalized BM25 [0, 1]
            c_norm = (raw_score - c_min) / c_diff
            
            # Normalized Log-PR [0, 1]
            lp_norm = (log_pr_vals[did] - lp_min) / lp_diff
            
            # Weighted combination
            combined[did] = self.weight_text * c_norm + self.weight_pagerank * lp_norm

        return combined

#===============================Not debugging======================
    @staticmethod
    def rank_top_k(scores: Dict[int, float], k: int = 10) -> List[int]:
        """
        Rank documents by score and return top-k doc IDs.
        """
        if not scores:
            return []

        ranked = sorted(scores.items(),key=lambda item: item[1],reverse=True)

        top_k = ranked[:k]

        return [doc_id for doc_id, _ in top_k]

    def get_top_k(self, query: str, k: int = 10) -> List[int]:
        scores = self.compute_ranking_scores(query)
        top10_docs = self.rank_top_k(scores, k)
        return top10_docs

    def get_top_100(self, query: str, k: int = 100) -> List[Tuple[int, str]]:
        scores = self.compute_ranking_scores(query)
        top100_docs = self.rank_top_k(scores, k)
        res = self.data_provider.get_titles_from_docIDs(top100_docs)
        return res










