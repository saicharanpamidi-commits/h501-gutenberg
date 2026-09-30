"""Tests for the tt_gutenberg package, using small made-up tables."""

import unittest
from unittest import mock

import pandas as pd

from tt_gutenberg import authors, transform


class TestGetData(unittest.TestCase):
    """Checks for transform.get_data."""

    def test_merges_authors_and_metadata(self):
        data = {
            "df_authors": pd.DataFrame({
                "gutenberg_author_id": [1, 2],
                "alias": ["Al", "Be"],
                "birthdate": [1800, 1700],
            }),
            "df_metadata": pd.DataFrame({
                "gutenberg_author_id": [1, 2],
                "author": ["A", "B"],
                "language": ["en", "fr"],
            }),
        }
        with mock.patch.object(transform, "DATA", data):
            df = transform.get_data()

        self.assertIn("author_alias", df.columns)
        self.assertIn("language", df.columns)
        self.assertEqual(len(df), 2)


class TestListAuthors(unittest.TestCase):
    """Checks for authors.list_authors."""

    def test_sorted_by_translation_count(self):
        fake = pd.DataFrame({
            "author_alias": ["X", "X", "X", "Y", "Z", "Z"],
            "language": ["en", "fr", "de", "en", "en", "fr"],
        })
        with mock.patch.object(authors, "get_data", return_value=fake):
            self.assertEqual(authors.list_authors(), ["X", "Z", "Y"])


if __name__ == "__main__":
    unittest.main()
