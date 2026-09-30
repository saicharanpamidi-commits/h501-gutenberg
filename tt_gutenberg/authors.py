"""Author listings and plots built on the merged Gutenberg data."""

import seaborn as sns
from tt_gutenberg.transform import (add_birth_century, add_translations,
                                    drop_missing, drop_unnamed, get_data)


def author_table():
    """Return one row per author, with their translation count."""
    df = add_translations(get_data())

    # get_data() has one row per book, so the same author repeats.
    # keep the first row for each author to get one row each.
    return df.drop_duplicates(subset=["gutenberg_author_id"])


def list_authors(by_languages=True, alias=True):
    """List Gutenberg authors, most translated first.

    Args:
        by_languages (bool): Sort by translation count, highest
            first. When False, keep the original file order.
        alias (bool): Return the `alias` column. When False, return
            the `author` column instead.

    Returns:
        list of str: The author names or aliases.
    """
    column = "alias" if alias else "author"

    df = author_table()

    # most rows have no alias at all, so those go before the list is
    # built, otherwise the result is full of NaN
    df = drop_missing(df, column)
    df = drop_unnamed(df, column)

    if by_languages:
        df = df.sort_values("n_languages", ascending=False)

    return df[column].tolist()


def plot_translations(over="birth_century"):
    """Bar plot of average translations per author birth century.

    Each bar is the mean number of languages for authors born in that
    century. Seaborn draws a 95% confidence interval on each bar.
    """
    df = author_table()
    df = drop_missing(df, "author")
    df = drop_unnamed(df, "author")
    df = df.dropna(subset=["birthdate"])
    df = add_birth_century(df)

    ax = sns.barplot(data=df, x=over, y="n_languages")
    ax.set_xlabel("Century of birth")
    ax.set_ylabel("Average number of languages")
    ax.set_title("Translations by birth century")
    ax.tick_params(axis="x", rotation=90)

    return ax
