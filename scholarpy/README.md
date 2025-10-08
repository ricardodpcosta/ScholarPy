
# Usage

ScholarPy includes a collection of tools, each designed for a specific task. The list below details the tools included in the toolkit and their usage instructions.

---

## 1. `scholarpy-search_links`

**Description:** Search public scholarly CV links from HTML pages. It has two modes of operation:

1. If argument 'base_url' is set, search institutional profile pages from the provided HTML page(s) (argument 'html_urls') matching the base_url pattern and then visit each institutional profile page to search public scholarly CV links. Useful when the provided HTML page(s) correspond(s) to a list of members, each with a link to an institutional page, where public scholarly CV links are contained.
2. If argument 'base_url' is empty, directly search public scholarly CV links inside the provided HTML page(s).

To avoid server overload and subsequent client IP blocking, a delay is applied between HTTP/HTTPS requests.

**Usage:** Run `scholarpy-search_links --help` on the command line.

**Arguments:**
* `--html_urls`   : Input HTML file(s) or URL(s), separated by commas (required).
* `--base_url`    : Base URL for institutional profile pages (optional, default: none).
* `--links_limit` : Limit number of links to retrieve (optional, default: 200).
* `--page_pause`  : Delay in seconds between HTTP/HTTPS requests (optional, default: 3).
* `--output_file` : Output TXT file containing the found links (optional, default: 'links.txt').

**Output:** A TXT file containing a list of links is saved to disk.

---

## 2. `collect_data.py`

**Description:** Collect relevant textual data from public scholarly CV links. The process is divided into three steps:
1. Read an input file containing a list of public scholarly CV links.
2. Visit each link and scrape the data on relevant fields, such as titles
   of fundings, projects, works, outcomes, and journals/conferences.
3. Clean and condense the data, keeping only alphabetic characters and spaces
   without repetition.
Scraping is performed with Selenium instead of Requests because some public
scholarly CV pages may load dynamically and are not fully accessible via static
HTML parsing. To avoid server overload and subsequent client IP blocking,
a delay is applied between HTTP/HTTPS requests.

**Usage:** Run `scholarpy-collect-data --help` on the command line.

**Arguments:**
* `--links_file`  : Input TXT file containing a list of public scholarly CV links (required).
* `--page_pause`  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
* `--output_file` : Output TXT file containing the collected data (optional, default: 'data.txt').

**Output:**
A TXT file containing all collected text from the public scholarly CV links is saved to disk.

---

## 3. `analise_words.py`

**Description:** Analyse relevant scientific words from collected data. The process is divided into two steps:
1. Read an input file containing data.
2. Lemmatise, filter, and count words.
Words are lemmatised (normalised) and filtered to remove common English and Portuguese stopwords, as well as domain-generic words.

**Usage:** Run `scholarpy-analise-words --help` on the command line.

**Arguments:**
* `--data_file`   : Input TXT file containing collected text (required).
* `--output_file` : Output CSV file containing words and their counts (optional, default: 'words.csv').

**Output:** A CSV file with words and counts is saved to disk.

---

## 4. `plot_wordcloud.py`

**Description:** Generate wordcloud visualisations from word frequency data. It generates two images:
1. A standard wordcloud plot containing all words with a gradient colour.
2. A recoloured version of the same layout, where special words are coloured with a custom colour.
The word layout remains identical between both images, allowing for easy comparison, while only the colours differ.

**Usage:** Run `scholarpy-plot-wordcloud --help` on the command line.

**Arguments:**
* `--words_file`      : Input CSV file with words and counts (required).
* `--plot_colourmap`  : Matplotlib colourmap for gradient colouring (optional, default: 'viridis').
* `--plot_maxwords`   : Limit number of words to plot (optional, default: 200).
* `--special_words`   : Comma-separated list of words to highlight in the wordcloud (optional, default: none).
* `--special_colour`  : Colour to highlight special words (optional, default: 'green').
* `--output_file`     : Output PNG file containing the wordcloud (optional, default: 'wordcloud.png').

**Output:** A PNG image of the generated wordcloud is saved to disk. If special words are provided, a second image is saved to disk.
