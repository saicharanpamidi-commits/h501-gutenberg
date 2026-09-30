"""Author listings and plots built on the merged Gutenberg data."""

import seaborn as sns
from tt_gutenberg import transform
from tt_gutenberg.transform import (add_birth_century, add_translations,
                                    alias_column, drop_missing,
                                    drop_unnamed, get_data, name_column)


def diag(where, error, df):
    """DIAG: one-line report of what a function actually received."""
    message = str(error)
    if message.startswith("DIAG"):
        message = message[len("DIAG "):]
    return RuntimeError(
        f"DIAG {where}: {type(error).__name__}: {message}; "
        f"df={type(df).__name__} cols={list(getattr(df, 'columns', []))}; "
        f"authors.get_data={type(get_data).__name__}; "
        f"transform.get_data={type(transform.get_data).__name__}")


def author_table(df):
    """Return one row per author, with their translation count."""
    df = add_translations(df)
    return df.drop_duplicates(subset=[name_column(df)])


def list_authors(by_languages=True, alias=True):
    """List Gutenberg authors, most translated first.

    Args:
        by_languages (bool): Sort by translation count, highest
            first. When False, keep the original file order.
        alias (bool): Return the alias column. When False, return the
            author name column instead.

    Returns:
        list of str: The author names or aliases.
    """
    raw = None
    try:
        raw = get_data()
        df = author_table(raw)
        column = alias_column(df) if alias else name_column(df)

        # most rows have no alias at all, so those go before the list
        # is built, otherwise the result is full of NaN
        df = drop_missing(df, column)
        df = drop_unnamed(df, column)

        if by_languages:
            df = df.sort_values("n_languages", ascending=False)

        return df[column].tolist()
    except Exception as error:
        raise diag("list_authors", error, raw) from error


def plot_prep(over="birth_century"):
    """Build the data frame that `plot_translations` draws."""
    raw = None
    try:
        raw = get_data()
        df = author_table(raw)
        key = name_column(df)

        df = drop_missing(df, key)
        df = drop_unnamed(df, key)

        if over == "birth_century":
            df = df.dropna(subset=["birthdate"])
            df = add_birth_century(df)

        return df
    except Exception as error:
        raise diag("plot_prep", error, raw) from error


def plot_translations(over="birth_century"):
    """Bar plot of average translations per author birth century.

    Each bar is the mean number of languages for authors born in that
    century. Seaborn draws a 95% confidence interval on each bar.
    """
    df = plot_prep(over)

    ax = sns.barplot(data=df, x=over, y="n_languages")
    ax.set_xlabel("Century of birth")
    ax.set_ylabel("Average number of languages")
    ax.set_title("Translation Count Over Birth Century")
    ax.tick_params(axis="x", rotation=90)

    return ax
