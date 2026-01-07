import csv
import gzip
import pickle
from pathlib import Path
from typing import Dict, List


class PageRankProvider:
    def __init__(self, base_dir: str, pr_subdir: str = "pr"):
        self.base_dir = Path(base_dir)
        self.pr_dir = self.base_dir / pr_subdir
        # no in-memory caching: only store base paths
        self.pr_dir = self.pr_dir


    def get_pagerank(self, doc_ids: List[int]) -> Dict[int, float]:
        """
        Read PageRank scores for a list of document IDs. Always read from source.

        Returns a dict mapping each requested doc_id to its pagerank (float).
        Missing IDs map to 0.0.
        """
        out: Dict[int, float] = {int(d): 0.0 for d in doc_ids}

        # check pickle candidates (prefer pkl files)
        candidates = []
        if self.pr_dir.exists() and self.pr_dir.is_dir():
            candidates += sorted(self.pr_dir.glob("*.pkl"))
            candidates += sorted(self.pr_dir.glob("*.pickle"))
            csv_candidates = sorted(list(self.pr_dir.glob("*.csv")) + list(self.pr_dir.glob("*.csv.gz")) + list(self.pr_dir.glob("part-*.csv.gz")))

        pr_base_pkl = self.base_dir / 'pagerank.pkl'
        pr_base_pickle = self.base_dir / 'pagerank.pickle'
        if pr_base_pkl.exists():
            candidates.insert(0, pr_base_pkl)
        if pr_base_pickle.exists():
            candidates.insert(0, pr_base_pickle)

        # try pickles first
        for p in candidates:
            try:
                with open(p, 'rb') as f:
                    data = pickle.load(f)
                if isinstance(data, dict):
                    for d in list(out.keys()):
                        # support int or str keys in pickle
                        out[d] = float(data.get(d, data.get(str(d), out[d])))
                    return out
            except Exception:
                continue
        return out
