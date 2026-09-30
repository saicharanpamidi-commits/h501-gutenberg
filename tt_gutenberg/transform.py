"""Loading and joining for the TidyTuesday Gutenberg data."""

import pandas as pd

# the folder holding the TidyTuesday Gutenberg CSV files
DATA = ("https://raw.githubusercontent.com/rfordatascience/"
        "tidytuesday/main/data/2025/2025-06-03/")


def data_path(name):
    """Return the location of one Gutenberg CSV file.

    `DATA` is normally the folder holding the files, but it can also
    be a mapping of short names to locations, so the loaders keep
    working if the source is pointed somewhere else.
    """
    if isinstance(DATA, dict):
        return DATA[name]
    return f"{DATA}gutenberg_{name}.csv"


def load_authors():
    """Load the authors table (one row per Gutenberg author)."""
    return pd.read_csv(data_path("authors"))


def load_metadata():
    """Load the book metadata (one row per Gutenberg book)."""
    return pd.read_csv(data_path("metadata"), low_memory=False)


def get_data():
    """Merge the authors and metadata tables into one data frame.

    Each row is a book, with that book's author details joined on.
    """
    authors = load_authors()
    metadata = load_metadata()

    return metadata.merge(authors, on="gutenberg_author_id", how="left")


def name_column(df):
    """Return the column holding author names.

    Both source files have an `author` column, so a plain merge
    renames them `author_x` and `author_y`. This finds whichever one
    is present.
    """
    for column in ["author", "author_y", "author_x", "alias"]:
        if column in df.columns:
            return column
    raise KeyError("no author name column found")


def count_translations(df):
    """Count the distinct languages for each author."""
    key = name_column(df)
    counts = df.groupby(key)["language"].nunique()
    return counts.rename("n_languages").reset_index()


def add_translations(df):
    """Add an `n_languages` column to a merged data frame."""
    if "n_languages" in df.columns:
        return df
    counts = count_translations(df)
    return df.merge(counts, on=name_column(df), how="left")


def drop_missing(df, column):
    """Drop rows where `column` is missing or only whitespace."""
    cleaned = df.dropna(subset=[column]).copy()
    return cleaned[cleaned[column].astype(str).str.strip() != ""]


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
