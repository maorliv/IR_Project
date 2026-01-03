from data_provider.DataProvider import DataProvider


if __name__ == "__main__":
    dp = DataProvider(r"C:\Users\maor livni\PycharmProjects\IR_Project\mini_index")

    term = "history"
    pl = dp.get_posting_list(term)

    print(f"Posting list size for '{term}':", len(pl))
    print("First 5 entries:", pl[:5])

    if pl:
        doc_id = pl[0][0]
        print("Sample doc_id:", doc_id)
        print("PageRank:", dp.get_pagerank(doc_id))
