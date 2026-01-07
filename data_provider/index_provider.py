import pickle
from pathlib import Path
from typing import Optional, List, Dict

from inverted_index_colab import read_posting_list


class IndexProvider:
    def __init__(self, base_dir: str, postings_subdir: str = "postings_gcp"):
        self.base_dir = Path(base_dir)
        self.postings_dir = self.base_dir / postings_subdir
        # Do not keep index or postings cached in memory.
        # All reads will load index metadata from disk on demand.
        self.index = None
        self.N = 6348910

    def get_posting_list(self, terms: List[str]) -> Dict[str, List]:
        """Return posting lists for multiple terms as a dict term -> posting_list."""
        base_for_postings = self.postings_dir if self.postings_dir.exists() else self.base_dir
        idx = self._load_index()
        out: Dict[str, List] = {}
        if idx is None:
            for t in terms:
                out[t] = []
            return out
        for t in terms:
            out[t] = read_posting_list(inverted=idx, base_dir=base_for_postings, w=t)
        return out

    def get_N(self) -> int:
        return self.N

    # def get_N(self) -> int:
    #     # compute fresh corpus size by scanning posting lists
    #     idx = self._load_index()
    #     if idx is None:
    #         return 0
    #     docs = set()
    #     base_for_postings = self.postings_dir if self.postings_dir.exists() else self.base_dir
    #     try:
    #         iterator = idx.posting_lists_iter(base_for_postings)
    #     except TypeError:
    #         iterator = idx.posting_lists_iter()
    #     for _, pl in iterator:
    #         for doc_id, _ in pl:
    #             docs.add(doc_id)
    #     return len(docs)

    def get_df(self, terms: List[str]) -> Dict[str, int]:
        """Return document frequencies for multiple terms as a dict term->df."""
        idx = self._load_index()
        out: Dict[str, int] = {}
        if idx is None:
            for t in terms:
                out[t] = 0
            return out
        dfmap = getattr(idx, 'df', {}) or {}
        for t in terms:
            out[t] = int(dfmap.get(t, 0))
        return out

    def _load_index(self):
        # load index metadata afresh from disk and merge any posting_locs
        idx_path = self.postings_dir / "index.pkl"
        index = None
        if idx_path.exists():
            try:
                with open(idx_path, "rb") as f:
                    index = pickle.load(f)
            except Exception:
                index = None

        if self.postings_dir.exists() and self.postings_dir.is_dir():
            for pl_path in sorted(self.postings_dir.glob("*_posting_locs.pickle")):
                try:
                    with open(pl_path, "rb") as f:
                        pl = pickle.load(f)
                    if not isinstance(pl, dict):
                        continue
                    if index is not None:
                        if hasattr(index, "posting_locs") and isinstance(index.posting_locs, dict):
                            index.posting_locs.update(pl)
                        else:
                            setattr(index, "posting_locs", getattr(index, "posting_locs", {}) or {})
                            index.posting_locs.update(pl)
                except Exception:
                    continue

        return index


