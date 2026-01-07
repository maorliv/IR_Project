from typing import List, Dict

from data_provider.data_provider import DataProvider
from text_processor.query_tokenize import QueryTokenize
from ranker.tf_idf import TfIdf
from ranker.cosine_similarity import CosineSimilarity

class SearchController:
    def __init__(self, base_dir: str, query: str):
        self.data_provider = DataProvider(base_dir=base_dir)
        self.query = QueryTokenize()
        self.tf_idf = TfIdf()

    def query_to_tokens(self, query: str) -> List[str]:
        return self.query.tokenize(query)

    def tokens_df(self, tokens: List[str]) -> Dict[str, int]:
        return self.data_provider.get_df(tokens)

    def tokens_postings(self, tokens: List[str]):
        return self.data_provider.get_posting_list(tokens)

    def corpus_size(self) -> int:
        return self.data_provider.corpus_size()

    def compute_tfidf(self, query: str):
        """Tokenize query, fetch posting lists, df and N, compute tf-idf.

        Returns: dict mapping doc_id -> {term: tfidf}
        """
        tokens = self.query_to_tokens(query)
        if not tokens:
            return {}
        postings = self.tokens_postings(tokens)
        df_map = self.tokens_df(tokens)
        N = self.corpus_size()
        return self.tf_idf.compute(postings=postings, df_map=df_map, N=N)

    def calc_query_tf_idf(self, query: str) -> Dict[str, float]:
        """
        Compute TF-IDF for the query itself (term frequencies from the query only).

        Parameters:
        - tokens: tokenized query (after stopword removal)

        Returns:
        - dict mapping term -> tfidf (tf is raw count in query)
        """
        tokens = self.query_to_tokens(query)

        if not tokens:
            return {}
        from collections import Counter
        import math

        tf_counts = Counter(tokens)
        terms = list(tf_counts.keys())
        df_map = self.tokens_df(terms)
        N = self.corpus_size()

        # delegate query TF-IDF calculation to TfIdf utility
        return self.tf_idf.compute_query_tfidf(tf_counts=tf_counts, df_map=df_map, N=N)

    def compute_cosine_scores(self,query: str) -> Dict[int, float]:
        """
        Compute cosine similarity scores between the query TF-IDF vector and
        provided document TF-IDF vectors. Returns a mapping doc_id -> score.

        This method delegates pure computation to `CosineSimilarity` and does
        not access any DAO or files.
        """
        doc_tfidfs = self.compute_tfidf(query)
        query_tfidf = self.calc_query_tf_idf(query)


        return CosineSimilarity.compute(query_vec=query_tfidf, doc_vecs=doc_tfidfs)




#===============================Not debugging======================
    @staticmethod
    def rank_top_k(scores: Dict[int, float], k: int = 10) -> List[int]:
        """
        Rank documents by score and return top-k doc IDs.
        """
        if not scores:
            return []

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        top_k = ranked[:k]

        return [doc_id for doc_id, _ in top_k]

    def get_top_k(self, query: str, k: int = 10) -> List[int]:
        scores = self.compute_cosine_scores(query)
        top10_docs = self.rank_top_k(scores, k)
        return top10_docs











