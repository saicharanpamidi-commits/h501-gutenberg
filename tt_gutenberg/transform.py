"""Loading and merging the TidyTuesday Project Gutenberg data."""

import pandas as pd

# where each table comes from. a value can be a CSV location or an
# already-loaded data frame.
DATA = {
    "df_authors": ("https://raw.githubusercontent.com/rfordatascience/"
                   "tidytuesday/main/data/2025/2025-06-03/"
                   "gutenberg_authors.csv"),
    "df_metadata": ("https://raw.githubusercontent.com/rfordatascience/"
                    "tidytuesday/main/data/2025/2025-06-03/"
                    "gutenberg_metadata.csv"),
}


def read_table(source):
    """Return a data frame, reading it from a CSV if needed."""
    if isinstance(source, pd.DataFrame):
        return source
    return pd.read_csv(source, low_memory=False)


def get_data():
    """Merge the authors and metadata tables on the author id.

    The result has one row per book, with the author's alias and
    birthdate joined on. It renames `alias` to `author_alias`, so the
    alias can't be mistaken for the `author` column.
    """
    authors = read_table(DATA["df_authors"])
    metadata = read_table(DATA["df_metadata"])

    # both real files have an `author` column. keep the one from the
    # metadata, so the merge does not create author_x and author_y
    authors = authors.drop(columns="author", errors="ignore")

    merged = pd.merge(authors, metadata, on="gutenberg_author_id")
    return merged.rename(columns={"alias": "author_alias"})
