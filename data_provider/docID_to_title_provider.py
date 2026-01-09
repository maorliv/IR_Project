# import pickle
# from pathlib import Path
# from typing import List, Tuple, Dict
#
#
# class TitleProvider:
#     def __init__(self, base_dir: str, titles_subdir: str = "id_to_title"):
#         self.base_dir = Path(base_dir)
#         self.titles_dir = self.base_dir / titles_subdir
#         self._titles: Dict[int, str] | None = None
#
#     def _load_titles(self):
#         if self._titles is not None:
#             return
#
#         pkl_path = self.titles_dir / "doc_id_to_title.pkl"
#         if not pkl_path.exists():
#             raise FileNotFoundError(f"Title file not found: {pkl_path}")
#
#         with open(pkl_path, "rb") as f:
#             data = pickle.load(f)
#
#         if not isinstance(data, dict):
#             raise ValueError("doc_id_to_title.pkl is not a dict")
#
#         # normalize keys to int
#         self._titles = {int(k): v for k, v in data.items()}
#
#     def get_titles_from_docIDs(self, doc_ids: List[int]) -> List[Tuple[int, str]]:
#         self._load_titles()
#
#         results = []
#         for doc_id in doc_ids:
#             title = self._titles.get(int(doc_id), "")
#             results.append((int(doc_id), title))
#
#         return results
#

import pickle
from pathlib import Path
from typing import List, Tuple, Dict


class TitleProvider:
    """
    Provides fast access to document titles by document ID.

    The entire doc_id -> title mapping is loaded into memory
    once during initialization and reused for all queries.
    """

    def __init__(self, base_dir: str, titles_subdir: str = "id_to_title"):
        self.base_dir = Path(base_dir)
        self.titles_dir = self.base_dir / titles_subdir

        pkl_path = self.titles_dir / "doc_id_to_title.pkl"
        if not pkl_path.exists():
            raise FileNotFoundError(f"Title file not found: {pkl_path}")

        with open(pkl_path, "rb") as f:
            data = pickle.load(f)

        if not isinstance(data, dict):
            raise ValueError("doc_id_to_title.pkl is not a dict")

        # Normalize keys to int for consistent lookups
        self._titles: Dict[int, str] = {
            int(doc_id): title for doc_id, title in data.items()
        }
        # print("LOADING TITLES")

    def get_titles_from_docIDs(self, doc_ids: List[int]) -> List[Tuple[int, str]]:
        """
        Return a list of (doc_id, title) tuples for the given document IDs.
        """
        results: List[Tuple[int, str]] = []

        for doc_id in doc_ids:
            did = int(doc_id)
            title = self._titles.get(did, "")
            results.append((did, title))

        return results



