# ScholarPy

**Extract, analyse, and visualise research insights from scholarly profiles with web scraping and data mining in Python.**

---

## Overview

ScholarPy is a Python toolkit for extracting relevant data, analysing textual information, and visualising research insights from public scholarly profiles, such as ORCID and CienciaVitae. It integrates **web browsing**, **web scraping**, **data mining**, and **data visualisation** using various Python libraries to provide meaningful insights into the research activities and outputs of individual researchers or research teams.

The toolkit offers a collection of modular tools to:

* Discover public scholarly profiles on institutional webpages.
* Extract relevant data from public scholarly profiles (currently supporting ORCID and CienciaVitae).
* Analyse textual information using **natural language processing (NLP)**.
* Visualise research insights through meaningful infographic representations.

<br>

<img src="images/pipeline.png" alt="ScholarPy pipeline" width="90%"/>

---

### Concepts

ScholarPy is built upon two core concepts:

- **Web scraping**: The process of automatically extracting data from websites. ScholarPy uses scraping to collect scholarly information from dynamic sources such as ORCID and CiênciaVitae profiles.  

- **Data mining**: The practice of analysing large sets of text or structured data to uncover patterns, trends, and insights. In ScholarPy, it transforms raw profile data into meaningful research indicators. 

---

## Features

This Python toolkit is based on advanced data processing and artificial intelligence modules:

* **Selenium**: Automates web browsing tasks, allowing the script to interact with dynamically generated content and enabling the extraction of data even when the content is loaded asynchronously with JavaScript. Essential for accessing ORCID and CiênciaVitae profiles.

* **BeautifulSoup**: Parses and navigates the HTML/XML content retrieved from webpages. It converts raw HTML/XML into a tree structure, allowing selective extraction of tags, attributes, and text with high precision.

* **SpaCy**: A state-of-the-art natural language processing (NLP) library. It supports tokenisation, lemmatisation, part-of-speech tagging, and stopword filtering in multiple languages (including English and Portuguese), making it ideal for processing scholarly texts.

* **Matplotlib**: A comprehensive data visualisation library. It provides tools to generate static and interactive plots, enabling the creation of custom graphs, trend plots, and word clouds that highlight the most relevant research insights from research profiles.


---

## Requirements

ScholarPy requires **Python 3.10+** and the following modules:

* [Selenium](https://pypi.org/project/selenium/).
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/). 
* [lxml](https://pypi.org/project/lxml/).
* [spaCy](https://spacy.io/).
  * (Required) English model (`en_core_web_sm`).
  * (Optional) Portuguese model (`pt_core_news_sm`).  
* [Matplotlib](https://pypi.org/project/matplotlib/). 
* [WordCloud](https://pypi.org/project/wordcloud/).

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ricardodpcosta/ScholarPy.git
cd ScholarPy
````

2. Install required packages via [pip](https://pypi.org/project/pip/):

```bash
pip install -r requirements.txt
```

3. Download the spaCy language models (English required, Portuguese optional):

```bash
python -m spacy download en_core_web_sm
python -m spacy download pt_core_news_sm
```

---

## Usage

ScholarPy provides various scripts, each with a specific purpose. Below are instructions for running each of them.

### 1. `search_links.py`

**Description:** Search public scholarly CV links from HTML pages. It has two modes of operation:
1. If BASE_URL (option --base) is set, search researcher profile pages from the provided HTML page(s) (option --html) matching the BASE_URL pattern and then visit each researcher profile page to search public scholarly CV links. Useful when the provided HTML page(s) correspond(s) to a list of researchers with links to individual pages, where public scholarly CV links are contained.
2. If BASE_URL is empty, directly search public scholarly CV links inside the provided HTML page(s).
To avoid server overload and subsequent client IP blocking, a delay is applied between HTTP/HTTPS requests.

**Usage:**
```bash
python search_links.py --html <HTML_FILE_OR_URL> [--base <BASE_URL>] [--out <OUTPUT_FILE>] [--limit <N>] [--pause <SECONDS>]
```

**Arguments:**
* `--html`   : Input HTML file(s) or URL(s), separated by commas (required).
* `--base`   : Base URL for researcher profile pages (optional, leave empty for direct mode).
* `--limit`  : Limit number of links to retrieve (optional, default=200).
* `--pause`  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
* `--out`    : Output TXT file containing the found links (optional, default: `links.txt`).

**Output:** A TXT file containing a list of links (one per line).

---

### 2. `extract_data.py`

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
* `--links`  : Input TXT file containing a list of public scholarly CV links (one per line).
* `--pause`  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
* `--out`    : Output TXT file containing the extracted textual data (optional, default: `data.txt`).

**Output:** A TXT file containing all extracted text from the profiles, cleaned and normalised.

---

### 3. `process_words.py`

**Description:** Analyse relevant scientific words from extracted data. The process is divided into two steps:
1. Read an input file containing data.
2. Lemmatise, filter and count words.
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

### 4. `plot_wordcloud.py`

**Description:** Generate word cloud visualisations from word frequency data. It generated two images:
1. A standard word cloud plot containing all words with a gradient colour.
2. A recoloured version of the same layout, where special words are highlighted with a custom colour.
The word layout remains identical between both images, allowing for easy comparison, while only the colours differ.

**Usage:**
```bash
python plot_wordcloud.py --words <WORDS_CSV_FILE> [--colormap <COLORMAP>] [--maxwords <MAXWORDS>] [--special <WORDS>] [--highlight <COLOR>] [--out <OUTPUT_FILE>]
```

**Arguments:**
* `--words`       : Input CSV file with words and counts (required).
* `--colormap`    : Matplotlib colourmap for gradient colouring (optional, default: `viridis`).
* `--maxwords`    : Limit number of words to plot (optional, default: 200).
* `--special`     : Comma-separated list of words to highlight in the word cloud (optional, default: none).
* `--highlight`   : Colour to highlight special words (optional, default: `green`).
* `--out`         : Output PNG file containing the word cloud (optional, default: `wordcloud.png`).

**Output:** A PNG image of the generated word cloud. If `--special` is provided, a second image is generated with highlighted words.

---

## Project Structure

```
ScholarPy/
│
├─ scripts/                 # Python scripts included in the toolkit
│   ├─ search_links.py      # Search public scholarly CV links from HTML or URLs
│   ├─ extract_data.py      # Scrape data from public scholarly CV pages
│   ├─ process_words.py     # Process text, lemmatise, filter stopwords, count words
│   └─ plot_wordcloud.py    # Generate word cloud visualisations from processed words
│
├─ examples/                # Example cases with running scripts
│
├─ requirements.txt         # Python dependencies for installation
├─ README.md                # Project overview, installation, usage instructions
└─ LICENSE                  # License file (MIT)

```

---

## License

MIT License – see [LICENSE](LICENSE) for details.

---

## Author

**Ricardo Costa** – [rcosta@dep.uminho.pt](mailto:rcosta@dep.uminho.pt)

