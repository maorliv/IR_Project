from evaluation.gold_standard_evaluator import GoldStandardEvaluator
from evaluation.evaluator import Evaluator
from controllers.SearchController import SearchController

gold_standard = GoldStandardEvaluator("queries_train.json")
# train_gold, test_gold = gold_standard.split_train_test()
all_queries = gold_standard.get_all_queries()

controller = SearchController(base_dir='data')
evaluator = Evaluator(gold_standard,controller)

def main():
    score = evaluator.evaluate_average_precision_at_10(all_queries)
    print(f"Average Precision@10 = {score:.4f}")


if __name__ == '__main__':
    main()