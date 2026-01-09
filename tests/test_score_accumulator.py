from controllers.SearchController import SearchController
from text_processor.query_tokenize import QueryTokenize
from ranker.score_accumulator import ScoreAccumulator


def main():
    sc = SearchController(base_dir='data')
    qt = QueryTokenize()
    q = 'Mount Everest climbing expeditions'
    acc = ScoreAccumulator()
    # compute_ranking_scores returns final scores, but test originally called compute_cosine_and_pr_scores
    # which we renamed to compute_ranking_scores.
    scores = sc.compute_ranking_scores(query=q)
    print('ScoreAccumulator and SearchController integration smoke test OK. Sample scores:', list(scores.items())[:5])
    print("the best 10 are:", sc.get_top_k(q))


if __name__ == '__main__':
    main() # run the test
