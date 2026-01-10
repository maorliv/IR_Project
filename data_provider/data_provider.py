from typing import List

from .index_provider import IndexProvider
from .pagerank_provider import PageRankProvider
from .docID_to_title_provider import TitleProvider



class DataProvider:
    """Compatibility wrapper that composes the three new providers.
    
    Loads data from GCS bucket.
    """
    def __init__(self, bucket_name: str, postings_subdir: str = "postings_gcp", pr_subdir: str = "pr", titles_subdir: str = "id_to_title" ):
        self.index_provider = IndexProvider(bucket_name=bucket_name, index_prefix=postings_subdir)
        self.pagerank_provider = PageRankProvider(bucket_name=bucket_name, pr_subdir=pr_subdir)
        self.title_provider = TitleProvider(bucket_name=bucket_name, titles_subdir=titles_subdir)


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

    def get_titles_from_docIDs(self, doc_ids: List[int]) -> List[tuple]:
        return self.title_provider.get_titles_from_docIDs(doc_ids)

    def get_titles_from_docIDs(self, doc_ids: List[int]):
        return self.title_provider.get_titles_from_docIDs(doc_ids)