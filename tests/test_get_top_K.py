from controllers.SearchController import SearchController



def main():
    sc = SearchController(base_dir='data', query='')
    q = 'Mount Everest climbing expeditions'
    print("the best 10 are:", sc.get_top_k(q))


if __name__ == '__main__':
    main() # run the test
