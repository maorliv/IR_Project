from controllers.SearchController import SearchController



def main():
    q = 'Mount Everest climbing expeditions'
    BUCKET_NAME = "ir-maor-2025-bucket"
    search_controller = SearchController(bucket_name=BUCKET_NAME)
    print(search_controller.get_query_term_weights(query=q))
    print('BM25.compute_query_weights tests OK')


if __name__ == '__main__':
    main()
