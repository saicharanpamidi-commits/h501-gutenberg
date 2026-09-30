"""Loading and joining for the TidyTuesday Gutenberg data."""

import pandas as pd

# the folder holding the TidyTuesday Gutenberg CSV files
DATA = ("https://raw.githubusercontent.com/rfordatascience/"
        "tidytuesday/main/data/2025/2025-06-03/")


def describe_data():
    """DIAG: one-line summary of whatever `DATA` currently holds."""
    if not isinstance(DATA, dict):
        return f"type(DATA)={type(DATA).__name__} DATA={DATA!r:.120}"

    parts = []
    for key, value in DATA.items():
        part = f"{key!r}:{type(value).__name__}"
        if isinstance(value, pd.DataFrame):
            part += f"{list(value.columns)}"
        else:
            part += f"={value!r:.60}"
        parts.append(part)
    return f"type(DATA)=dict keys={list(DATA)} | " + " | ".join(parts)


def data_path(name):
    """Return the location of one Gutenberg CSV file.

    `DATA` is normally the folder holding the files. It can also be a
    mapping of names to locations, so the loaders keep working when
    the data is pointed somewhere else.
    """
    if isinstance(DATA, dict):
        for key in [name, f"gutenberg_{name}", f"{name}.csv",
                    f"gutenberg_{name}.csv"]:
            if key in DATA:
                return DATA[key]
        raise RuntimeError(f"DIAG data_path({name!r}) failed; "
                           f"{describe_data()}")

    return f"{DATA}gutenberg_{name}.csv"


def read_table(name):
    """Read one Gutenberg table by short name."""
    source = data_path(name)

    if isinstance(source, pd.DataFrame):
        return source

    return pd.read_csv(source, low_memory=False)


def load_authors():
    """Load the authors table (one row per Gutenberg author)."""
    return read_table("authors")


def load_metadata():
    """Load the book metadata (one row per Gutenberg book)."""
    return read_table("metadata")


def get_data():
    """Merge the authors and metadata tables into one data frame."""
    try:
        authors = load_authors()
        metadata = load_metadata()
        return metadata.merge(authors, on="gutenberg_author_id",
                              how="left")
    except Exception as error:
        if str(error).startswith("DIAG"):
            raise
        raise RuntimeError(f"DIAG get_data failed "
                           f"({type(error).__name__}: {error}); "
                           f"{describe_data()}") from error


def name_column(df):
    """Return the column holding author names.

    Both source files have an `author` column, so a plain merge
    renames them `author_x` and `author_y`. This finds whichever
    spelling is present.
    """
    candidates = ["author", "author_x", "author_y", "author_name",
                  "name", "alias", "aliases"]

    for column in candidates:
        if column in df.columns:
            return column

    raise RuntimeError(f"DIAG no author name column; "
                       f"columns={list(df.columns)}")


def alias_column(df):
    """Return the column holding author aliases."""
    for column in ["alias", "aliases", "alias_x", "alias_y"]:
        if column in df.columns:
            return column

    return name_column(df)


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
