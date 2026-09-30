"""Author listings built from the Gutenberg translation counts."""

from tt_gutenberg.data import author_translations, drop_missing


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

    df = author_translations()

    # most rows have no alias at all, so those have to go before the
    # list is built, otherwise the result is full of NaN
    df = drop_missing(df, column)

    if by_languages:
        df = df.sort_values("n_languages", ascending=False)

    return df[column].tolist()
