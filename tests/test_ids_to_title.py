import unittest
from controllers.SearchController import SearchController

class TestIdsToTitle(unittest.TestCase):
    def setUp(self):
        # Assuming the project root is current working directory
        BUCKET_NAME = "ir-maor-2025-bucket"
        self.controller = SearchController(bucket_name=BUCKET_NAME)

    def test_get_top_100_returns_titles_structure(self):
        """
        Verify that get_top_100 returns a list of (doc_id, title) tuples,
        contains at most 100 results, and types are correct.
        """
        # 1. Use one real query taken from the Gold Standard file
        query = "Stonehenge prehistoric monument"

        # 2. Invoke the get_top_100 method with this query
        # We request 100 results
        results = self.controller.get_top_100(query, k=100)
        print(results[:10])


        # 3. Verify the output

        # - Is a list
        self.assertIsInstance(results, list, "Return value must be a list")

        # - Contains at most 100 results
        self.assertLessEqual(len(results), 100, "Should return at most 100 results")
        # Also check it returns something for this known query (sanity check)
        self.assertTrue(len(results) > 0, "Should return at least one result for a valid query")

        # - Each result is a tuple of the form (doc_id, title)
        for i, item in enumerate(results):
            self.assertIsInstance(item, tuple, f"Item at index {i} must be a tuple")
            self.assertEqual(len(item), 2, f"Item at index {i} must have length 2 (doc_id, title)")

            doc_id, title = item

            # - doc_id is an int
            self.assertIsInstance(doc_id, int, f"doc_id at index {i} must be an int")

            # - title is a str
            self.assertIsInstance(title, str, f"title at index {i} must be a str")

if __name__ == '__main__':
    unittest.main()




