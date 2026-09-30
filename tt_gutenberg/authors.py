"""Author listings and plots built on the merged Gutenberg data."""

import seaborn as sns
from tt_gutenberg.transform import get_data


def list_authors(by_languages=True, alias=True):
    """List Gutenberg authors, most translated first.

    Args:
        by_languages (bool): Sort by the number of distinct languages
            each author's books appear in, highest first. When False,
            keep the order the authors first appear in the data.
        alias (bool): Return author aliases. When False, return the
            author names instead.

    Returns:
        list of str: The author aliases or names.
    """
    column = "author_alias" if alias else "author"

    # most authors have no alias, so drop those rows rather than
    # listing NaN
    df = get_data().dropna(subset=[column])

    if by_languages:
        counts = df.groupby(column)["language"].nunique()
        return counts.sort_values(ascending=False).index.tolist()

    return df[column].drop_duplicates().tolist()


def plot_prep(over="birth_century"):
    """Build one row per author with a translation count and century.

    Drops placeholder authors such as "Anonymous", since they aren't
    real people with a birthdate. `over` is only there to match
    `plot_translations`; birth century is the only option so far.
    """
    df = get_data().dropna(subset=["author", "birthdate"])
    df = df[~df["author"].isin(["Anonymous", "Various", "Unknown"])]

    per_author = df.groupby("author").agg(
        n_languages=("language", "nunique"),
        birthdate=("birthdate", "first"),
    )

    # floor divide by 100 then multiply back: 1753 becomes 1700
    century = (per_author["birthdate"] // 100) * 100
    per_author["birth_century"] = century.astype(int)

    return per_author.reset_index()


def plot_translations(over="birth_century"):
    """Bar plot of average translation count by author birth century.

    Seaborn's barplot shows the mean of each group and draws a 95%
    confidence interval on each bar by default.
    """
    df = plot_prep(over)

    ax = sns.barplot(data=df, x=over, y="n_languages")
    ax.set_title("Translation Count Over Birth Century")
    ax.set_xlabel("Birth century")
    ax.set_ylabel("Average number of languages")
    ax.tick_params(axis="x", rotation=90)

    return ax
