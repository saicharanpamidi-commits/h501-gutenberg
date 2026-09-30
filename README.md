# h501-gutenberg

Lists Project Gutenberg authors by how many languages their work has
been translated into, using the
[TidyTuesday Gutenberg dataset](https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-06-03/readme.md).

## Package layout

```
tt_gutenberg/
├── __init__.py    exposes get_data, list_authors and plot_translations
├── transform.py   get_data(): loads the two CSVs and merges them
└── authors.py     list_authors(), plot_prep() and plot_translations()
```

`authors.py` gets its data from `transform.get_data()`, so the loading
and merging happen in one place.

## Usage

```python
from tt_gutenberg.authors import list_authors

list_authors(by_languages=True, alias=True)
```

## Environment

```
python 3.12

packages:
- ipykernel
- pandas
- seaborn
```
