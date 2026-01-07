from controllers.SearchController import SearchController
from evaluation.gold_standard_evaluator import GoldStandardEvaluator


class Evaluator:
    def __init__(self, gold_standard:GoldStandardEvaluator, controller:SearchController):
        self.gold = gold_standard
        self.controller = controller

    def get_ranked_results(self,query):
        self.controller.compute_cosine_scores(query)




