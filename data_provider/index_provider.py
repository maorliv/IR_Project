from typing import List, Dict

from inverted_index_gcp import InvertedIndex


class IndexProvider:
    """
    Provides access to the inverted index.

    Index metadata (index.pkl + posting locations) is loaded once during
    initialization and kept in memory. Posting lists themselves are read
    from disk on demand.
    """

    def __init__(self, bucket_name: str, index_prefix: str = "postings_gcp"):
        self.bucket_name = bucket_name
        self.index_prefix = index_prefix
        
        # Load the index from GCS
        self.index = InvertedIndex.read_index(self.index_prefix, "index", self.bucket_name)

        # corpus size (as provided by the course)
        self.N: int = 6_348_910

    def get_posting_list(self, terms: List[str]) -> Dict[str, List]:
        """Return posting lists for multiple terms as a dict term -> posting_list."""
        out: Dict[str, List] = {}
        if self.index is None:
            # Should not happen if initialized correctly, but as a safeguard
            return {t: [] for t in terms}

        for t in terms:
            out[t] = self.index.read_a_posting_list(self.index_prefix, t, self.bucket_name)
        return out

    def get_N(self) -> int:
        return self.N


    def get_df(self, terms: List[str]) -> Dict[str, int]:
        """Return document frequencies for multiple terms as a dict term->df."""
        out: Dict[str, int] = {}
        if self.index is None:
            return {t: 0 for t in terms}
            
        dfmap = getattr(self.index, 'df', {}) or {}
        for t in terms:
            out[t] = int(dfmap.get(t, 0))
        return out


