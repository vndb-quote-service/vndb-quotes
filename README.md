# VNDB Quotes

If you look carefully on [VNDB](https://vndb.org) footer, you will see a quote randomly selected from a VN.
This repo scrapes it every 30 minutes and saves it to CSV, TSV and JSON.

#### Differences between `csv_excel` and `csv`
According to [Python](https://docs.python.org/3/library/csv.html#csv.Dialect), there are differences between Unix styled CSV and Excel CSV.
You can read it up on their docs. The TSV may be a good alternative because you rarely (or never will) get quotes with a tab character.

#### License
The scraper itself is licensed under MIT. The quote files are public domain as I could not find licensing on VNDB.
