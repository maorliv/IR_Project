from ranker.tf_idf import TfIdf
from controllers.SearchController import SearchController
import math


def main():
    q = 'Mount Everest climbing expeditions'
    search_controller = SearchController(base_dir='data', query=q)
    print(search_controller.calc_query_tf_idf(query=q))
    print('TfIdf.compute_query_tfidf tests OK')


if __name__ == '__main__':
    main()
