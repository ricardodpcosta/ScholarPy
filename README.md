# ScholarPy

**A Python toolkit for collecting, analysing, and visualising research insights from public scholarly CVs with web scraping and data mining.**

<br>
<img src="gallery/scholarpy.png" alt="ScholarPy pipeline" width="20%"/>

---

## Overview

ScholarPy is a Python toolkit for collecting relevant data, analysing textual information, and visualising research insights from public scholarly CVs, such as ORCID and CienciaVitae. It integrates **web browsing**, **web scraping**, **data mining**, and **data visualisation** using various Python libraries to provide meaningful insights into the research activities and outputs of individual researchers or research teams.

The toolkit offers a collection of modular tools to:

* Discover public scholarly CVs on institutional webpages.
* Collect relevant data from public scholarly CVs (currently supporting ORCID and CienciaVitae).
* Analyse textual information using **natural language processing (NLP)**.
* Visualise research insights through meaningful infographic representations.

<br>
<img src="gallery/pipeline.png" alt="ScholarPy pipeline" width="100%"/>

---

## Concepts

ScholarPy is built upon two core concepts:

- **Web scraping**: The process of automatically extracting data from websites. ScholarPy implements web scraping to collect public scholarly CV information from online sources, such as ORCID and CiênciaVitae.  

- **Data mining**: The practice of analysing large sets of text or structured data to uncover patterns, trends, and insights. In ScholarPy, it transforms plain scholarly data into meaningful research indicators.

---

## Features

This Python toolkit is based on advanced data processing and artificial intelligence modules:

* **Selenium**: Automates web browsing tasks, allowing scripts to interact with dynamically generated content and enabling the extraction of data even when the content is loaded asynchronously with JavaScript. Essential for accessing public scholarly CV pages.

* **BeautifulSoup**: Parses and navigates the HTML/XML content retrieved from webpages. It converts raw HTML/XML into a tree structure, allowing selective extraction of data of interest, such as tags, attributes, and text with high precision and efficiency.

* **SpaCy**: A state-of-the-art natural language processing (NLP) library. It supports tokenisation, lemmatisation, part-of-speech tagging, and stopword filtering in multiple languages (including English and Portuguese), making it ideal for processing scholarly texts.

* [**Matplotlib**](https://matplotlib.org/): A comprehensive data visualisation library. It provides tools to generate static and interactive plots, enabling the creation of custom graphs, trend plots, and wordclouds that highlight the most relevant research insights from research profiles.

<br>
<div align="center">
  <table>
    <tr>
      <td align="center"><img src="gallery/wordcloud.png" width="100%"></td>
      <td align="center"><img src="gallery/special_wordcloud.png" width="100%"></td>
    </tr>
  </table>
</div>
     
---

## Requirements

ScholarPy requires **Python 3.10+** and the following modules:

* [Selenium](https://pypi.org/project/selenium/).
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/).
* [lxml](https://pypi.org/project/lxml/).
* [spaCy](https://spacy.io/).
  * (Required) English model (`en_core_web_lg`).
  * (Optional) Portuguese model (`pt_core_news_lg`).  
* [Matplotlib](https://pypi.org/project/matplotlib/).
* [WordCloud](https://pypi.org/project/wordcloud/).

---

## Installation

Check whether your system provides a [**Python**](https://www.python.org/downloads/) installation with version 3.10 or above, and the [pip](https://pypi.org/project/pip/) package installer is available on your Python installation.

It is generally recommended to install **ScholarPy** and its dependencies in a virtual environment to avoid modifying the system state. Several options for creating a virtual environment are available, including:

* [**venv**](https://docs.python.org/3/library/venv.html): a Python module for creating lightweight virtual environments, each with their own independent set of packages installed in their site directory. Since **venv** is part of the Python standard library, no installation is required.

* [**conda**](https://anaconda.org/anaconda/conda): an open source package management system and environment management system for installing multiple versions of software packages and their dependencies and switching easily between them. Usually, **conda** needs to be [installed](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) previously.

Follow these steps to install **ScholarPy**:

**1. Clone the repository:**

```bash
git clone https://github.com/ricardodpcosta/ScholarPy.git
cd ScholarPy
```

**2. Create a virtual environment:**

* Using **venv**:

```bash
python -m venv virtual
source virtual/bin/activate
```

* Using **conda**:

```bash
conda env create -f environment.yml
conda activate virtual
```

> **NOTE:** Skip this step for installing **ScholarPy** and its dependencies directly on top of your base Python installation.

**3. Update the package installation environment:**

```bash
pip install --upgrade pip setuptools wheel
```

**4. Install ScholarPy via pip:**

```bash
pip install .
```

Alternatively, to install in editable/development mode:

```bash
pip install -e .
```

If desired, dependencies can be installed before **ScholarPy**:

```bash
pip install -r requirements.txt
```

**5. Download the spaCy language models:**

```bash
python -m spacy download en_core_web_lg
python -m spacy download pt_core_news_lg
```

*(English required, Portuguese optional)*

**6. Verify ScholarPy is installed:**

```bash
scholarpy --help
```

Alternatively, from within a Python program or interactive shell:

```python
import scholarpy
print("ScholarPy successfully installed!")
```

If no errors are displayed, the installation is complete and **ScholarPy** is correctly installed.

**7. Start using ScholarPy:**

Once installed, you can import ScholarPy in any Python program:

```python
from scholarpy import core
core.collect_data(links_file="links.txt", output_file="data.txt")
```

Alternatively, execute the tools directly from a command line, for example:

```bash
scholarpy collect_data --links_file="links.txt" --output_file="data.txt"
```

**8. Deactivate the virtual environment:**

* Using **venv**:

```bash
source virtual/bin/deactivate
```

* Using **conda**:

```bash
conda deactivate
```

> **NOTE:** For reactivating the previous virtual environment created for **ScholarPy** (without reinstalling), run from the project's root directory `source virtual/bin/activate` (if using **venv**) or `conda activate virtual` (if using **conda**).

---

## Structure

```
ScholarPy/
│
├─ scholarpy/               # Main source package
│   ├─ __init__.py          # Package initializer
│   ├─ core.py              # Core functions and shared utilities
│   ├─ ...                  # Additional functional modules and tool wrappers
│   └─ README.md            # Package-level documentation and usage details
│
├─ examples/                # Example workflows and demonstration scripts
│
├─ setup.py                 # Package configuration and installation script
├─ requirements.txt         # Python dependency list for installation
├─ README.md                # Project overview, installation, and usage guide
├─ CONTRIBUTING.md          # Contribution guidelines and best practices
└─ LICENSE                  # Software license information
```

---

## Workflow

A typical workflow within ScholarPy is as follows (check the examples):

1. Run `scholarpy search_links` to collect public scholarly CV links (currently supporting **ORCID** and **CienciaVitae**).

   * If you already have a prepared list of links, skip this step and proceed directly to **Step 2**.
   * The input can be a single link (for individual analysis) or a list of links (for group/collective analysis).

2. Run `scholarpy extract_data` to scrape relevant textual data from the retrieved scholarly CV pages.

3. Perform various analyses of the extracted text data using the available tools (currently `scholarpy analyse_words`).

4. Generate various data visualisations using the available tools (currently `scholarpy plot_wordcloud`).

---

## Contributing

Contributions are encouraged in all forms, including the addition of tools, refinement of scripts, enhancement of documentation, and resolution of issues.
For detailed guidelines, refer to [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

📧 [Ricardo Costa](mailto:rcosta\@dep.uminho.pt)  
🌐 [Academic page](https://ricardodpcosta.github.io/)
