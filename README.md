# PyScholar

**Extract, analyse, and visualise research insights on scholarly profiles with web scraping and data mining in Python.**

---

## Overview

ScholarPy is a Python toolkit to extract, process, and visualize data from public scholarly profiles, such as ORCID and CienciaVitae. It combines **web scraping**, **text mining**, and **data visualization** to generate meaningful insights on researchers’ publications, projects, and outputs.

The toolkit allows you to:

* Extract CVs from ORCID or CienciaVitae profiles.
* Analyze textual data using **lemmatization** and **stopword filtering**.
* Generate **word clouds** and frequency counts of scientific terms.
* Highlight specific keywords for tailored visualization.

---

## Features

* **Web Scraping**: Automatically retrieve data from ORCID and CienciaVitae profiles using Selenium and BeautifulSoup.
* **Text Mining**: Clean, lemmatize, and filter scientific terms.
* **Word Cloud Generation**: Visualize frequent terms with customizable colors and colormaps.
* **Modular Workflow**: Separate scripts for data extraction and analysis.

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
