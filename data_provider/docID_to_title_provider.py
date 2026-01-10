import pickle
from typing import List, Tuple, Dict
from google.cloud import storage


class TitleProvider:
    """
    Provides fast access to document titles by document ID from GCS.
    """

    def __init__(self, bucket_name: str, titles_subdir: str = "id_to_title"):
        self.bucket = storage.Client().bucket(bucket_name)
        self.titles_path = f"{titles_subdir}/doc_id_to_title.pkl"

        blob = self.bucket.blob(self.titles_path)
        with blob.open("rb") as f:
            data = pickle.load(f)

        if not isinstance(data, dict):
            raise ValueError("doc_id_to_title.pkl is not a dict")

        # Normalize keys to int for consistent lookups
        self._titles: Dict[int, str] = {
            int(doc_id): title for doc_id, title in data.items()
        }

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



