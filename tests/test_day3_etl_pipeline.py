import unittest

from src.ingestion.day3_etl_pipeline import (
    normalized_name,
    valid_website,
    valid_date,
    score_is_consistent,
)


class TestDay3ETLPipeline(unittest.TestCase):

    # Website URL validation
    def test_valid_https_website(self):
        self.assertTrue(
            valid_website("https://example.com")
        )

    def test_valid_http_website(self):
        self.assertTrue(
            valid_website("http://example.com")
        )

    def test_website_without_scheme_is_invalid(self):
        self.assertFalse(
            valid_website("example.com")
        )

    def test_empty_website_is_invalid(self):
        self.assertFalse(
            valid_website("")
        )

    def test_website_with_spaces_is_invalid(self):
        self.assertFalse(
            valid_website("https://example .com")
        )

    # Date validation
    def test_valid_date(self):
        self.assertTrue(
            valid_date("22-08-2026")
        )

    def test_invalid_date_format(self):
        self.assertFalse(
            valid_date("2026-08-22")
        )

    def test_impossible_date(self):
        self.assertFalse(
            valid_date("31-02-2026")
        )

    # Company name normalization
    def test_company_name_normalization(self):
        self.assertEqual(
            normalized_name("  PayU India  "),
            "payu india",
        )

    def test_company_name_case_normalization(self):
        self.assertEqual(
            normalized_name("WINGIFY"),
            "wingify",
        )

    # Prospect score validation
    def test_consistent_prospect_score(self):
        row = {
            "Company Size Score": "10",
            "B2B Fit Score": "20",
            "Technology Signal Score": "15",
            "Business Need Score": "25",
            "Recent Business Signal Score": "10",
            "Decision-Maker Score": "20",
            "Prospect Score": "100",
        }

        self.assertTrue(
            score_is_consistent(row)
        )

    def test_inconsistent_prospect_score(self):
        row = {
            "Company Size Score": "10",
            "B2B Fit Score": "20",
            "Technology Signal Score": "15",
            "Business Need Score": "25",
            "Recent Business Signal Score": "10",
            "Decision-Maker Score": "20",
            "Prospect Score": "95",
        }

        self.assertFalse(
            score_is_consistent(row)
        )

    def test_invalid_score_value(self):
        row = {
            "Company Size Score": "invalid",
            "B2B Fit Score": "20",
            "Technology Signal Score": "15",
            "Business Need Score": "25",
            "Recent Business Signal Score": "10",
            "Decision-Maker Score": "20",
            "Prospect Score": "100",
        }

        self.assertFalse(
            score_is_consistent(row)
        )


if __name__ == "__main__":
    unittest.main()