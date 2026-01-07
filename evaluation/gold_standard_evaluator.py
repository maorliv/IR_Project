import json
import random
from typing import Dict, List, Tuple


class GoldStandardEvaluator:
    """
    Responsible for:
    - Loading a gold standard JSON file
    - Splitting queries into train/test sets
    - Providing access to relevant documents per query
    """

    def __init__(self, gold_path: str):
        """
        Initialize evaluator by loading the gold standard file.

        gold_path: path to JSON file
        """
        self.gold = self._load_gold_standard(gold_path)

    # ---------- Private helpers ----------

    def _load_gold_standard(self, path: str) -> Dict[str, List[str]]:
        """
        Load gold standard JSON file.
        Format:
        {
            query: [doc_id1, doc_id2, ...]
        }
        """
        with open(path, "r", encoding="utf-8") as f:
            gold = json.load(f)

        if not isinstance(gold, dict):
            raise ValueError("Gold standard must be a dictionary")

        for query, docs in gold.items():
            if not isinstance(query, str):
                raise ValueError("Query must be a string")
            if not isinstance(docs, list):
                raise ValueError("Relevant docs must be a list")

        return gold

    # ---------- Public API ----------

    def get_all_queries(self) -> List[str]:
        """Return all queries in the gold standard"""
        return list(self.gold.keys())

    def get_relevant_docs(self, query: str) -> List[str]:
        """Return relevant document IDs for a given query"""
        return self.gold.get(query, [])

    def split_train_test(self,train_size: int = 20,test_size: int = 10,seed: int = 42) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        Split queries into train and test sets.

        Returns:
        (train_gold, test_gold)
        """
        queries = self.get_all_queries()

        if train_size + test_size > len(queries):
            raise ValueError("Train + Test size exceeds number of queries")

        random.seed(seed)
        random.shuffle(queries)

        train_queries = queries[:train_size]
        test_queries = queries[train_size:train_size + test_size]

        train_gold = {q: self.gold[q] for q in train_queries}
        test_gold = {q: self.gold[q] for q in test_queries}

        return train_gold, test_gold
