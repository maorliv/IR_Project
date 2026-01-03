from text_processor.query_tokenize import QueryTokenize

if __name__ == "__main__":
    tp = QueryTokenize()
    query = "The History of Mount Everest and the People who Climbed It"
    print(tp.tokenize(query))
