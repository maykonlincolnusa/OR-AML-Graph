import unittest

from or_aml_graph import analyze_transactions, project_info


def tx(identifier, source, target, currency="BRL"):
    return {"id": identifier, "source_account_id": source, "destination_account_id": target,
            "amount": "10.00", "currency": currency,
            "occurred_at": "2026-01-01T10:00:00+00:00"}


class ProjectTest(unittest.TestCase):
    def test_detects_cycle_with_evidence(self):
        result = analyze_transactions([tx("1", "a", "b"), tx("2", "b", "c"), tx("3", "c", "a")])
        self.assertEqual(result["networks"][0]["cycles"][0]["transaction_ids"], ["1", "2", "3"])
        self.assertEqual(project_info()["status"], "reference-prototype")

    def test_isolates_currencies(self):
        result = analyze_transactions([tx("1", "a", "b", "BRL"), tx("2", "b", "a", "USD")])
        self.assertTrue(all(not network["cycles"] for network in result["networks"]))

    def test_reports_truncation_instead_of_hanging(self):
        result = analyze_transactions([tx("1", "a", "b"), tx("2", "b", "c")], max_expansions=1)
        self.assertTrue(result["networks"][0]["truncated"])


if __name__ == "__main__":
    unittest.main()
