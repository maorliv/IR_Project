from controllers.SearchController import SearchController


def main():
    # simple synthetic example
    # postings: term -> list of (doc_id, tf)

    q = 'Mount Everest climbing expeditions'
    BUCKET_NAME = "ir-maor-2025-bucket"
    search_controller = SearchController(bucket_name=BUCKET_NAME)
    print(len(search_controller.compute_doc_scores(query=q)))

if __name__ == '__main__':
    main()
