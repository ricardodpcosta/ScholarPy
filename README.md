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

### Concepts used

ScholarPy is built upon two core concepts:

- **Web scraping**: The process of automatically extracting data from websites. ScholarPy uses scraping to collect scholarly information from dynamic sources such as ORCID and CiênciaVitae profiles.  

- **Data mining**: The practice of analysing large sets of text or structured data to uncover patterns, trends, and insights. In ScholarPy, it transforms raw profile data into meaningful research indicators. 

---

## Features

This Python toolkit is based on advanced data processing and artificial intelligence packages:

* **Selenium**: Automates web browsing tasks, allowing the script to interact with dynamically generated content and enabling the extraction of data even when the content is loaded asynchronously with JavaScript. Essential for accessing ORCID and CiênciaVitae profiles.

* **BeautifulSoup**: Parses and navigates the HTML/XML content retrieved from webpages. It converts raw HTML/XML into a tree structure, allowing selective extraction of tags, attributes, and text with high precision.

* **SpaCy**: A state-of-the-art natural language processing (NLP) library. It supports tokenisation, lemmatisation, part-of-speech tagging, and stopword filtering in multiple languages (including English and Portuguese), making it ideal for processing scholarly texts.

* **Matplotlib**: A comprehensive data visualisation library. It provides tools to generate static and interactive plots, enabling the creation of custom graphs, trend plots, and word clouds that highlight the most relevant research insights from research profiles.


---

## Requirements

* Python 3.10+
* [Selenium](https://pypi.org/project/selenium/)
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
* [spaCy](https://spacy.io/) (`en_core_web_sm` model required)
* [WordCloud](https://pypi.org/project/wordcloud/)
* [Matplotlib](https://pypi.org/project/matplotlib/)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ScholarPy.git
cd ScholarPy
```

2. Install required packages:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## Usage

### 1. Extract CVs

```bash
python extract_profiles.py --html urls.txt --base "https://www.cienciavitae.pt" --out links.txt
```

* `--html` : File or URL containing profile links.
* `--base` : Base URL for individual researcher pages (optional).
* `--out` : Output file for extracted profile links.

### 2. Extract Text

```bash
python extract_text.py --links links.txt --out data.txt
```

* `--links` : Input file with profile URLs.
* `--out` : Output file containing raw text from profiles.

### 3. Analyze Words

```bash
python analyze_words.py --input data.txt --out words.csv
```

* `--input` : Text file with extracted profile content.
* `--out` : Output CSV file with word counts.

### 4. Generate Word Cloud

```bash
python generate_wordcloud.py --words words.csv --colormap viridis --special "AI,Machine Learning" --highlight green --out wordcloud.png
```

* `--words` : CSV file with word counts.
* `--colormap` : Colormap for word cloud (default: `viridis`).
* `--special` : Comma-separated words to highlight.
* `--highlight` : Highlight color for special words.
* `--out` : Output image file.

---

## Project Structure

```
ScholarPy/
│
├─ extract_profiles.py      # Scrapes ORCID/CienciaVitae links
├─ extract_text.py          # Extracts text from profiles
├─ analyze_words.py         # Cleans, lemmatizes, and counts words
├─ generate_wordcloud.py    # Creates word cloud visualizations
├─ requirements.txt         # Required Python packages
└─ README.md                # Project documentation
```

---

## License

MIT License – see [LICENSE](LICENSE) for details.

---

## Author

**Ricardo Costa** – [rcosta@dep.uminho.pt](mailto:rcosta@dep.uminho.pt)

---

Se quiseres, posso criar **uma versão ainda mais curta e “GitHub ready”** com badges, highlights e links diretos para instalação e exemplos, que fica ótima na primeira página do repositório. Queres que eu faça?
