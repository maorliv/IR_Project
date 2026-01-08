from controllers.SearchController import SearchController
from evaluation.gold_standard_evaluator import GoldStandardEvaluator
from evaluation.precision_at_10 import PrecisionAt_10
import time
from typing import Iterable, List


class Evaluator:
    def __init__(self, gold_standard: GoldStandardEvaluator, controller: SearchController):
        self.gold = gold_standard
        self.search_controller = controller
        self.precision = PrecisionAt_10()

    def evaluate_average_precision_at_10(self, queries: Iterable[str]) -> float:
        """Evaluate queries, printing per-query runtime and Precision@10.

        Prints clearly labeled outputs for each query (runtime and Precision@10),
        then prints the final Average Precision@10 and whether the efficiency
        and quality requirements are satisfied.
        """
        total = 0.0
        n = 0
        runtimes: List[float] = []

        print("--- Evaluation: per-query runtime and Precision@10 ---")

        for query in queries:
            n += 1
            print(f'Query: "{query}"')

            t0 = time.perf_counter()
            ranked_docs = self.search_controller.get_top_k(query)
            t1 = time.perf_counter()

            runtime = t1 - t0
            runtimes.append(runtime)

            # normalize relevant doc ids to ints for correct comparison
            relevant_raw = self.gold.get_relevant_docs(query)
            relevant_ints: List[int] = []
            for d in relevant_raw:
                try:
                    relevant_ints.append(int(d))
                except Exception:
                    # ignore malformed ids
                    continue

            p_at_10 = self.precision.precision_at_10(ranked_docs, relevant_ints)
            total += p_at_10

            print(f"Runtime: {runtime:.6f} seconds")
            print(f"Precision@10: {p_at_10:.4f}")
            print("----------------------------------------")

        avg = total / n if n else 0.0
        print(f"Average Precision@10 on test set: {avg:.4f}")

        quality_ok = avg > 0.1
        efficiency_ok = all(r <= 35.0 for r in runtimes)

        print(f"Quality requirement satisfied: {'YES' if quality_ok else 'NO'}")
        print(f"Efficiency requirement satisfied: {'YES' if efficiency_ok else 'NO'}")

        return avg
#
# (clean single implementation above)
