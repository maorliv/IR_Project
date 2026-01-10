from controllers.SearchController import SearchController


def main():
    BUCKET_NAME = "ir-maor-2025-bucket"
    sc = SearchController(bucket_name=BUCKET_NAME)
    q = 'Stonehenge prehistoric monument'
    print("the best 10 are:", sc.get_top_100(q)[:10])


if __name__ == '__main__':
    main() # run the test
