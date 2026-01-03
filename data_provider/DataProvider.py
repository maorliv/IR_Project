import pickle
from pathlib import Path
from inverted_index_colab import InvertedIndex, read_posting_list

class DataProvider:
    def __init__(self, base_dir: str):
        """
        base_dir:
            Directory containing:
            - index.pkl        (inverted index metadata)
            - *.bin            (posting lists)
            - pagerank.pkl     (PageRank scores)
        """
        self.base_dir = Path(base_dir)

        # Load inverted index metadata (BODY only)
        self.index = InvertedIndex.read_index(base_dir=self.base_dir, name="index") #reed only index.pkl(inverted index metadata)

        # Load PageRank dictionary
        with open(self.base_dir / "pagerank.pkl", "rb") as f:
            self.pagerank = pickle.load(f)


    # ---------- Inverted Index ----------

    def get_posting_list(self, term: str):
        return read_posting_list(inverted=self.index,base_dir=self.base_dir,w=term)

    # ---------- PageRank ----------

    def get_pagerank(self, doc_id: int) -> float:
        """
        Return PageRank score for a document.
        """
        return self.pagerank.get(doc_id, 0.0)