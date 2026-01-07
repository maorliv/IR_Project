from data_provider.data_provider import DataProvider
from text_processor.query_tokenize import QueryTokenize


def main():
    dp = DataProvider(r"C:\Users\maor livni\PycharmProjects\IR_Project\data")

    # full query to test (tokenized)
    q = "Mount Everest climbed food"
    qt = QueryTokenize()
    tokens = qt.tokenize(q)

    # get_posting_list for multiple tokens
    pls = dp.get_posting_list(tokens)
    # print(pls["mount"])
    assert isinstance(pls, dict), "posting lists should be a dict"
    # pick first token that has postings
    term = None
    for t in tokens:
        if pls.get(t):
            term = t
            break
    assert term is not None, f"no posting list found for any token in {tokens}"
    pl = pls[term]
    assert isinstance(pl, list)
    assert len(pl) > 0, f"posting list for '{term}' should not be empty"
    assert isinstance(pl[0][0], int) and isinstance(pl[0][1], int), "posting entries must be (int,int)"
    print(f"get_posting_list({tokens}) -> {len(pl)} entries for '{term}' OK")

    # get_pagerank for multiple doc ids
    doc_ids = [entry[0] for entry in pl[:3]]
    pr_map = dp.get_pagerank(doc_ids)
    assert isinstance(pr_map, dict), "pagerank result should be a dict"
    assert all(isinstance(v, float) for v in pr_map.values()), "pagerank values must be floats"
    for did in doc_ids:
        assert did in pr_map
        assert pr_map[did] >= 0.0
    print(f"get_pagerank({doc_ids}) -> { [pr_map[d] for d in doc_ids] } OK")

    # get_df for multiple tokens
    print(tokens)
    df_map = dp.get_df(tokens)
    assert isinstance(df_map, dict), "df result should be a dict"
    assert df_map[term] == len(pl), f"df({term}) should equal posting list length ({df_map[term]} != {len(pl)})"
    print(f"get_df({tokens}) -> {df_map} OK")



if __name__ == "__main__":
    main()
