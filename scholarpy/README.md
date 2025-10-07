
# Usage

ScholarPy includes a collection of tools, each designed for a specific task. The list below details the tools included in the toolkit and their usage instructions.

---

## 1. `search_links.py`

**Description:** Search public scholarly CV links from HTML pages. It has two modes of operation:

1. If BASE_URL (option `--base`) is set, search researcher profile pages from the provided HTML page(s) (option `--html`) matching the BASE_URL pattern and then visit each researcher profile page to search public scholarly CV links. Useful when the provided HTML page(s) correspond(s) to a list of researchers with links to individual pages, where public scholarly CV links are contained.
2. If BASE_URL is empty, directly search public scholarly CV links inside the provided HTML page(s).

To avoid server overload and subsequent client IP blocking, a delay is applied between HTTP/HTTPS requests.

**Usage:**
```bash
python search_links.py --html <INPUT_HTML_FILE_OR_URL> [--base <BASE_URL>] [--out <OUTPUT_FILE>] [--limit <N>] [--pause <SECONDS>]
```

**Arguments:**
* `--html`   : Input HTML file(s) or URL(s), separated by commas (required).
* `--base`   : Base URL for researcher profile pages (optional, leave empty for direct mode).
* `--limit`  : Limit number of links to retrieve (optional, default=200).
* `--pause`  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
* `--out`    : Output TXT file containing the found links (optional, default: `links.txt`).

**Output:** A TXT file containing a list of links (one per line).

---

## 2. `extract_data.py`

**Description:** Extract relevant textual data from public scholarly CV links. The process is divided into three steps:

1. Read an input file containing a list of public scholarly CV links.
2. Visit each link and scrape the data on relevant fields, such as titles of fundings, projects, works, outcomes, and journals/conferences.
3. Clean and condense the data, keeping only alphabetic characters and spaces without repetition.

Scraping is performed with Selenium instead of Requests because some public scholarly CV pages may load dynamically and are not fully accessible via static HTML parsing. To avoid server overload and subsequent client IP blocking, a delay is applied between HTTP/HTTPS requests.

**Usage:**
```bash
python extract_data.py --links <INPUT_LINKS_FILE> [--out <OUTPUT_FILE>] [--pause <SECONDS>]
```

**Arguments:**
* `--links`  : Input TXT file containing a list of public scholarly CV links (required, one per line).
* `--pause`  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
* `--out`    : Output TXT file containing the extracted textual data (optional, default: `data.txt`).

**Output:** A TXT file containing all extracted text from the profiles, cleaned and normalised.

---

## 3. `analise_words.py`

**Description:** Analyse relevant scientific words from extracted data. The process is divided into two steps:

1. Read an input file containing data.
2. Lemmatise, filter, and count words.

Words are lemmatised (normalised) and filtered to remove common English and Portuguese stopwords, as well as domain-generic words.

**Usage:**
```bash
python process_words.py --data <INPUT_DATA_FILE> [--out <OUTPUT_FILE>]
```

**Arguments:**
* `--data`  : Input TXT file containing extracted text (required).
* `--out`   : Output CSV file containing words and their counts (optional, default: `words.csv`).

**Output:** A CSV file with columns `word` and `count`, containing processed and filtered words.

---

## 4. `plot_wordcloud.py`

**Description:** Generate word cloud visualisations from word frequency data. It generated two images:

1. A standard word cloud plot containing all words with a gradient colour.
2. A recoloured version of the same layout, where special words are highlighted with a custom colour.

The word layout remains identical between both images, allowing for easy comparison, while only the colours differ.

**Usage:**
```bash
python plot_wordcloud.py --words <INPUT_WORDS_FILE> [--colormap <COLORMAP>] [--maxwords <MAXWORDS>] [--special <WORDS>] [--highlight <COLOR>] [--out <OUTPUT_FILE>]
```

**Arguments:**
* `--words`       : Input CSV file with words and counts (required).
* `--colormap`    : Matplotlib colourmap for gradient colouring (optional, default: `viridis`).
* `--maxwords`    : Limit number of words to plot (optional, default: 200).
* `--special`     : Comma-separated list of words to highlight in the word cloud (optional, default: none).
* `--highlight`   : Colour to highlight special words (optional, default: `green`).
* `--out`         : Output PNG file containing the word cloud (optional, default: `wordcloud.png`).

**Output:** A PNG image of the generated word cloud. If `--special` is provided, a second image is generated with highlighted words.
