"""Author listings and plots built on the merged Gutenberg data."""

import seaborn as sns
from tt_gutenberg.transform import (add_birth_century, add_translations,
                                    drop_missing, drop_unnamed, get_data,
                                    name_column)


def author_table():
    """Return one row per author, with their translation count."""
    df = add_translations(get_data())
    return df.drop_duplicates(subset=[name_column(df)])


def list_authors(by_languages=True, alias=True):
    """List Gutenberg authors, most translated first.

    Args:
        by_languages (bool): Sort by translation count, highest
            first. When False, keep the original file order.
        alias (bool): Return the `alias` column. When False, return
            the author name column instead.

    Returns:
        list of str: The author names or aliases.
    """
    df = author_table()
    column = "alias" if alias else name_column(df)

    # most rows have no alias at all, so those go before the list is
    # built, otherwise the result is full of NaN
    df = drop_missing(df, column)
    df = drop_unnamed(df, column)

    if by_languages:
        df = df.sort_values("n_languages", ascending=False)

    return df[column].tolist()


def plot_prep(over="birth_century"):
    """Build the data frame that `plot_translations` draws.

    One row per author, with a translation count and, when plotting
    over birth century, a `birth_century` column.
    """
    df = author_table()
    df = drop_missing(df, name_column(df))
    df = drop_unnamed(df, name_column(df))

    if over == "birth_century":
        df = df.dropna(subset=["birthdate"])
        df = add_birth_century(df)

    return df


def plot_translations(over="birth_century"):
    """Bar plot of average translations per author birth century.

    Each bar is the mean number of languages for authors born in that
    century. Seaborn draws a 95% confidence interval on each bar.
    """
    df = plot_prep(over)

    ax = sns.barplot(data=df, x=over, y="n_languages")
    ax.set_xlabel("Century of birth")
    ax.set_ylabel("Average number of languages")
    ax.set_title("Translations by birth century")
    ax.tick_params(axis="x", rotation=90)

    return ax
