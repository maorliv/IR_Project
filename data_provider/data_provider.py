import csv
import sys
import gzip
import pickle
from pathlib import Path
from typing import Dict, List

from .index_provider import IndexProvider
from .pagerank_provider import PageRankProvider



class DataProvider:
    """Compatibility wrapper that composes the three new providers.

    Existing callers can continue to use `DataProvider(base_dir)` and call
    `get_posting_list` and `get_pagerank`. Internally this delegates to the
    new `IndexProvider`, `PageRankProvider` and `IndexStatsProvider` classes.
    """
    def __init__(self, base_dir: str, postings_subdir: str = "postings_gcp", pr_subdir: str = "pr"):
        self.index_provider = IndexProvider(base_dir=base_dir, postings_subdir=postings_subdir)
        self.pagerank_provider = PageRankProvider(base_dir=base_dir, pr_subdir=pr_subdir)


    def get_posting_list(self, terms: List[str]):
        # expect a list of terms; protect against accidental string input
        if isinstance(terms, (str, bytes)):
            raise TypeError("terms must be a list of strings, not a single string")
        terms = list(terms)
        return self.index_provider.get_posting_list(terms)

    def get_pagerank(self, doc_ids: List[int]):
        # expect a list of document ids
        if isinstance(doc_ids, (str, bytes, int)):
            raise TypeError("doc_ids must be a list of ints, not a single value")
        ids = list(doc_ids)
        return self.pagerank_provider.get_pagerank(ids)

    def get_df(self, terms: List[str]):
        # expect a list of terms; protect against accidental string input
        if isinstance(terms, (str, bytes)):
            raise TypeError("terms must be a list of strings, not a single string")
        terms = list(terms)
        return self.index_provider.get_df(terms)

    def corpus_size(self) -> int:
        return self.index_provider.get_N()