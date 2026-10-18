import unittest

from or_aml_graph import find_cycles, project_info


class ProjectSmokeTest(unittest.TestCase):
    def test_project_metadata(self) -> None:
        self.assertEqual(project_info()["status"], "starter")

    def test_finds_cycle(self) -> None:
        rows = [
            {"source_account_id": "a", "destination_account_id": "b"},
            {"source_account_id": "b", "destination_account_id": "c"},
            {"source_account_id": "c", "destination_account_id": "a"},
        ]
        self.assertEqual(find_cycles(rows), [["a", "b", "c", "a"]])



if __name__ == "__main__":
    unittest.main()

