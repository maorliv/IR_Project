from controllers.SearchController import SearchController
from ranker.tf_idf import TfIdf
import math


def main():
    # simple synthetic example
    # postings: term -> list of (doc_id, tf)

    q = 'Mount Everest climbing expeditions'
    search_controller = SearchController(base_dir='data', query=q)
    # print(search_controller.compute_tfidf(query=q))
    print(len(search_controller.compute_tfidf(query=q)))

if __name__ == '__main__':
    main()
