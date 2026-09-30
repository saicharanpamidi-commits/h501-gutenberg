"""Seaborn plots for the Gutenberg translation counts."""

import seaborn as sns
from tt_gutenberg.data import author_translations, drop_missing


def add_birth_century(df):
    """Add a birth_century column, so 1753 becomes 1700."""
    with_century = df.copy()

    # floor divide by 100 chops off the last two digits, and
    # multiplying back by 100 turns 17 into 1700
    century = (with_century["birthdate"] // 100) * 100
    with_century["birth_century"] = century.astype(int)

    return with_century


def drop_unnamed(df):
    """Drop placeholder authors such as Anonymous and Various."""
    placeholders = ["Anonymous", "Various", "Unknown"]
    return df[~df["author"].isin(placeholders)]


def plot_translations(over="birth_century"):
    """Bar plot of average translations per author birth century.

    Each bar is the mean number of languages for authors born in
    that century. Seaborn draws a 95% confidence interval on each
    bar by default.
    """
    df = author_translations()
    df = drop_missing(df, "author")
    df = drop_unnamed(df)
    df = df.dropna(subset=["birthdate"])
    df = add_birth_century(df)

    ax = sns.barplot(data=df, x=over, y="n_languages")
    ax.set_xlabel("Century of birth")
    ax.set_ylabel("Average number of languages")
    ax.set_title("Translations per author by birth century")
    ax.tick_params(axis="x", rotation=90)

    return ax
