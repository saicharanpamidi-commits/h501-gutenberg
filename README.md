# h501-gutenberg

Lists Project Gutenberg authors by how many languages their work has
been translated into, using the
[TidyTuesday Gutenberg dataset](https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-06-03/readme.md).

## Package layout

```
tt_gutenberg/
├── __init__.py    exposes list_authors and plot_translations
├── data.py        loads the CSVs and counts translations per author
├── authors.py     list_authors(), built on data.py
└── plots.py       plot_translations(), built on data.py
```

`authors.py` and `plots.py` both call functions in `data.py`, so the
loading and joining logic is written once.

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
