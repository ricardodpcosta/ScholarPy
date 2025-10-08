# ===============================================================
# ScholarPy - Package configuration file
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# Description: Setup file with definitions for PyPI
# ===============================================================

from setuptools import setup, find_packages

setup(
    name="scholarpy",
    version="0.1.0",
    author="Ricardo Costa",
    author_email="rcosta@dep.uminho.pt",
    description="A Python toolkit for collecting, analysing, and visualising research \
                    insights from public scholarly CVs with web scraping and data mining.",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0",
        "beautifulsoup4>=4.12",
        "lxml>=4.9",
        "langdetect>=1.0.9",
        "deep-translator>=1.11.4",
        "spacy>=3.5",
        "matplotlib>=3.7",
        "wordcloud>=1.8"
    ],
    entry_points={
        "console_scripts": [
            "scholarpy=scholarpy.__main__:main",
            "scholarpy-search-links=scholarpy.search_links:main",
            "scholarpy-collect-data=scholarpy.collect_data:main",
            "scholarpy-analyse-words=scholarpy.analyse_words:main",
            "scholarpy-plot-wordcloud=scholarpy.plot_wordcloud:main",
        ],
    },
)

# End of file
