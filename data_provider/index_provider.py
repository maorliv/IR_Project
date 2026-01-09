# import pickle
# from pathlib import Path
# from typing import Optional, List, Dict
#
# from inverted_index_colab import read_posting_list
#
#
# class IndexProvider:
#     def __init__(self, base_dir: str, postings_subdir: str = "postings_gcp"):
#         self.base_dir = Path(base_dir)
#         self.postings_dir = self.base_dir / postings_subdir
#         # Do not keep index or postings cached in memory.
#         # All reads will load index metadata from disk on demand.
#         self.index = None
#         self.N = 6348910
#
#     def get_posting_list(self, terms: List[str]) -> Dict[str, List]:
#         """Return posting lists for multiple terms as a dict term -> posting_list."""
#         base_for_postings = self.postings_dir if self.postings_dir.exists() else self.base_dir
#         idx = self._load_index()
#         out: Dict[str, List] = {}
#         if idx is None:
#             for t in terms:
#                 out[t] = []
#             return out
#         for t in terms:
#             out[t] = read_posting_list(inverted=idx, base_dir=base_for_postings, w=t)
#         return out
#
#     def get_N(self) -> int:
#         return self.N
#
#
#     def get_df(self, terms: List[str]) -> Dict[str, int]:
#         """Return document frequencies for multiple terms as a dict term->df."""
#         idx = self._load_index()
#         out: Dict[str, int] = {}
#         if idx is None:
#             for t in terms:
#                 out[t] = 0
#             return out
#         dfmap = getattr(idx, 'df', {}) or {}
#         for t in terms:
#             out[t] = int(dfmap.get(t, 0))
#         return out
#
#     def _load_index(self):
#         # load index metadata afresh from disk and merge any posting_locs
#         idx_path = self.postings_dir / "index.pkl"
#         index = None
#         if idx_path.exists():
#             try:
#                 with open(idx_path, "rb") as f:
#                     index = pickle.load(f)
#             except Exception:
#                 index = None
#
#         if self.postings_dir.exists() and self.postings_dir.is_dir():
#             for pl_path in sorted(self.postings_dir.glob("*_posting_locs.pickle")):
#                 try:
#                     with open(pl_path, "rb") as f:
#                         pl = pickle.load(f)
#                     if not isinstance(pl, dict):
#                         continue
#                     if index is not None:
#                         if hasattr(index, "posting_locs") and isinstance(index.posting_locs, dict):
#                             index.posting_locs.update(pl)
#                         else:
#                             setattr(index, "posting_locs", getattr(index, "posting_locs", {}) or {})
#                             index.posting_locs.update(pl)
#                 except Exception:
#                     continue
#
#         return index
#
#

import pickle
from pathlib import Path
from typing import List, Dict

from inverted_index_colab import read_posting_list


class IndexProvider:
    """
    Provides access to the inverted index.

    Index metadata (index.pkl + posting locations) is loaded once during
    initialization and kept in memory. Posting lists themselves are read
    from disk on demand.
    """

    def __init__(self, base_dir: str, postings_subdir: str = "postings_gcp"):
        self.base_dir = Path(base_dir)
        self.postings_dir = self.base_dir / postings_subdir

        # corpus size (as provided by the course)
        self.N: int = 6_348_910

        # load index metadata eagerly
        self._index = self._load_index()

        # base directory for posting files
        self._postings_base = self.postings_dir if self.postings_dir.exists() else self.base_dir

    def get_posting_list(self, terms: List[str]) -> Dict[str, List]:
        """
        Return posting lists for multiple terms as a dict: term -> posting_list.
        """
        out: Dict[str, List] = {}

        if self._index is None:
            for t in terms:
                out[t] = []
            return out

        for t in terms:
            out[t] = read_posting_list(
                inverted=self._index,
                base_dir=self._postings_base,
                w=t
            )

        return out

    def get_df(self, terms: List[str]) -> Dict[str, int]:
        """
        Return document frequencies for multiple terms as a dict: term -> df.
        """
        out: Dict[str, int] = {}

        if self._index is None:
            for t in terms:
                out[t] = 0
            return out

        dfmap = getattr(self._index, "df", {}) or {}
        for t in terms:
            out[t] = int(dfmap.get(t, 0))

        return out

    def get_N(self) -> int:
        return self.N

    def _load_index(self):
        """
        Load index metadata (index.pkl and posting locations) once.
        """
        idx_path = self.postings_dir / "index.pkl"
        index = None

        if idx_path.exists():
            with open(idx_path, "rb") as f:
                index = pickle.load(f)

        if index is None:
            return None

        # merge posting locations into index.posting_locs
        posting_locs = {}

        if self.postings_dir.exists() and self.postings_dir.is_dir():
            for pl_path in sorted(self.postings_dir.glob("*_posting_locs.pickle")):
                with open(pl_path, "rb") as f:
                    pl = pickle.load(f)
                if isinstance(pl, dict):
                    posting_locs.update(pl)

        if posting_locs:
            if hasattr(index, "posting_locs") and isinstance(index.posting_locs, dict):
                index.posting_locs.update(posting_locs)
            else:
                index.posting_locs = posting_locs

        return index
