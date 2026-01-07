from controllers.SearchController import SearchController
from text_processor.query_tokenize import QueryTokenize
from ranker.cosine_similarity import CosineSimilarity


def main():
    sc = SearchController(base_dir='data', query='')
    qt = QueryTokenize()
    q = 'Mount Everest climbing expeditions'
    cos = CosineSimilarity()
    scores = sc.compute_cosine_scores(query=q)
    print('CosineSimilarity.compute smoke test OK. Sample scores:', list(scores.items())[:5])
    print("the best 10 are:", sc.get_top_k(q))


if __name__ == '__main__':
    main() # run the test
