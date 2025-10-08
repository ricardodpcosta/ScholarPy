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
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0",
        "beautifulsoup4>=4.12",
        "spacy>=3.5",
        "matplotlib>=3.7",
        "wordcloud>=1.8",
    ],
    entry_points={
        "console_scripts": [
            "scholarpy-search-links=scholarpy.cli.search_links:main",
            "scholarpy-collect-data=scholarpy.cli.collect_data:main",
            "scholarpy-analyse-words=scholarpy.cli.analyse_words:main",
            "scholarpy-plot-wordcloud=scholarpy.cli.plot_wordcloud:main",
        ],
    },
)

# End of file
