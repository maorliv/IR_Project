import pickle
from typing import Dict, List
from google.cloud import storage


class PageRankProvider:
    """
    Provides access to PageRank scores for documents from GCS.
    """

    def __init__(self, bucket_name: str, pr_subdir: str = "pr"):
        self.bucket = storage.Client().bucket(bucket_name)
        self.pr_path = f"{pr_subdir}/pagerank.pkl"
        
        # Load from GCS
        # Note: blob.open requires google-cloud-storage >= 1.38.0
        # If older, we might need download_as_bytes -> io.BytesIO
        blob = self.bucket.blob(self.pr_path)
        with blob.open("rb") as f:
            data = pickle.load(f)

        if not isinstance(data, dict):
            raise ValueError("pagerank.pkl is not a dict")

        # normalize keys to int and values to float
        self._pagerank: Dict[int, float] = {
            int(doc_id): float(score)
            for doc_id, score in data.items()
        }

    def get_pagerank(self, doc_ids: List[int]) -> Dict[int, float]:
        """
        Return PageRank scores for the given document IDs.

        Missing document IDs are mapped to 0.0.
        """
        out: Dict[int, float] = {}

        for doc_id in doc_ids:
            did = int(doc_id)
            out[did] = self._pagerank.get(did, 0.0)

        return out
