"""Loading and joining for the TidyTuesday Gutenberg data."""

import pandas as pd


def base_url():
    """Return the folder that holds the TidyTuesday Gutenberg files."""
    return ("https://raw.githubusercontent.com/rfordatascience/"
            "tidytuesday/main/data/2025/2025-06-03/")


def load_authors():
    """Load the authors table (one row per Gutenberg author)."""
    return pd.read_csv(base_url() + "gutenberg_authors.csv")


def load_languages():
    """Load the table of languages each book appears in."""
    return pd.read_csv(base_url() + "gutenberg_languages.csv")


def load_metadata():
    """Load the book metadata, which links each book to an author."""
    return pd.read_csv(base_url() + "gutenberg_metadata.csv",
                       low_memory=False)


def count_translations():
    """Count the distinct languages each author appears in.

    A book can appear in several languages, so the languages table
    has one row per book per language. Joining it to the metadata
    brings in the author id, and counting the unique languages per
    author gives that author's translation count.
    """
    languages = load_languages()
    metadata = load_metadata()

    # only the two columns we need, and only rows that name an author
    books = metadata[["gutenberg_id", "gutenberg_author_id"]].dropna()

    merged = languages.merge(books, on="gutenberg_id")
    counts = merged.groupby("gutenberg_author_id")["language"].nunique()

    return counts.rename("n_languages").reset_index()


def author_translations():
    """Return the authors table with a translation count column."""
    authors = load_authors()
    counts = count_translations()

    merged = authors.merge(counts, on="gutenberg_author_id", how="left")
    merged["n_languages"] = merged["n_languages"].fillna(0).astype(int)

    return merged


def drop_missing(df, column):
    """Drop rows where `column` is missing or only whitespace."""
    cleaned = df.dropna(subset=[column]).copy()
    cleaned = cleaned[cleaned[column].str.strip() != ""]
    return cleaned
