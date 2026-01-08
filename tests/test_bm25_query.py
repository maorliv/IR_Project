from ranker.bm25 import BM25
from controllers.SearchController import SearchController
import math


def main():
    q = 'Mount Everest climbing expeditions'
    search_controller = SearchController(base_dir='data', query=q)
    print(search_controller.get_query_term_weights(query=q))
    print('BM25.compute_query_weights tests OK')


if __name__ == '__main__':
    main()
