from evaluation.gold_standard_evaluator import GoldStandardEvaluator

def main():
    evaluator = GoldStandardEvaluator("queries_train.json")

    train_gold, test_gold = evaluator.split_train_test()

    print("Train queries:", len(train_gold))
    print("Test queries:", len(test_gold))

    example_query = list(test_gold.keys())[0]
    print("Example query:", example_query)
    print("Relevant docs count:", len(test_gold[example_query]))

if __name__ == '__main__':
    main()