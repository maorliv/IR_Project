import re
from nltk.corpus import stopwords
from typing import List

class QueryTokenize:
    """
    Responsible for query text processing.
    Uses the exact same tokenization and stopword removal
    logic that was used during corpus indexing.
    """

    # Regular expression used in index creation
    RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)

    # English stopwords (NLTK)
    ENGLISH_STOPWORDS = frozenset(stopwords.words('english'))

    # Corpus-specific stopwords (Assignment 3)
    CORPUS_STOPWORDS = {
        "category", "references", "also", "external", "links",
        "may", "first", "see", "history", "people", "one", "two",
        "part", "thumb", "including", "second", "following",
        "many", "however", "would", "became"
    }

    # Unified stopword set
    ALL_STOPWORDS = ENGLISH_STOPWORDS.union(CORPUS_STOPWORDS)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes a query string using:
        - lowercase
        - regex-based tokenization
        - removal of english + corpus stopwords

        Parameters:
            text (str): raw query string

        Returns:
            List[str]: cleaned tokens
        """
        tokens = [
            token.group()
            for token in self.RE_WORD.finditer(text.lower())
            if token.group() not in self.ALL_STOPWORDS
        ]
        return tokens