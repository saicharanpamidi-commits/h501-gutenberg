"""Loading and joining for the TidyTuesday Gutenberg data."""

import numpy as np
import pandas as pd


def base_url():
    """Return the folder that holds the TidyTuesday Gutenberg files."""
    return ("https://raw.githubusercontent.com/rfordatascience/"
            "tidytuesday/main/data/2025/2025-06-03/")


def load_authors():
    """Load the authors table (one row per Gutenberg author)."""
    return pd.read_csv(base_url() + "gutenberg_authors.csv")


def load_metadata():
    """Load the book metadata (one row per Gutenberg book)."""
    return pd.read_csv(base_url() + "gutenberg_metadata.csv",
                       low_memory=False)


def get_data():
    """Merge the authors and metadata tables into one data frame.

    Each row is a book, with the author details joined on. Both files
    carry an `author` column, so the one from the authors table is
    dropped to avoid a duplicated column in the result.
    """
    authors = load_authors()
    metadata = load_metadata()

    authors = authors.drop(columns=["author"])

    return metadata.merge(authors, on="gutenberg_author_id", how="left")


def count_translations(df):
    """Count the distinct languages each author appears in."""
    counts = df.groupby("gutenberg_author_id")["language"].nunique()
    return counts.rename("n_languages").reset_index()


def add_translations(df):
    """Add an `n_languages` column to the merged data."""
    counts = count_translations(df)
    return df.merge(counts, on="gutenberg_author_id", how="left")


def drop_missing(df, column):
    """Drop rows where `column` is missing or only whitespace."""
    cleaned = df.dropna(subset=[column]).copy()
    return cleaned[cleaned[column].str.strip() != ""]


def add_birth_century(df):
    """Add a birth_century column, so 1753 becomes 1700."""
    with_century = df.copy()
    century = (with_century["birthdate"] // 100) * 100
    with_century["birth_century"] = century.astype(int)
    return with_century


def drop_unnamed(df, column):
    """Drop placeholder names such as Anonymous and Various."""
    placeholders = ["Anonymous", "Various", "Unknown"]
    return df[~df[column].isin(placeholders)]
