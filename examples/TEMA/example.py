#!/usr/bin/env python3
# ===============================================================
# ScholarPy - Example usage (Python)
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# ===============================================================
# Description:
# ------------
# Demonstrates the ScholarPy workflow using the Python package.
# Assumes ScholarPy is installed via pip and available as a module.
#
# Usage:
# ------
# python example.py
# ===============================================================

from scholarpy.core import (
    search_links,
    collect_data,
    analyse_words,
    plot_wordcloud
)

def main():
    # Step 1: Search public scholarly CV links
    search_links(
        html_urls="members.html",
        base_url="https://www.ua.pt/pt/p/",
        links_limit=50,
        output_file="links.txt"
    )
    # Step 2: Collect data from public scholarly CVs
    collect_data(
        links_file="links.txt",
        output_file="data.txt"
    )
    # Step 3: Analyse and process words
    analyse_words(
        data_file="data.txt",
        output_file="words.csv"
    )
    # Step 4: Generate word cloud visualization
    plot_wordcloud(
        words_file="words.csv",
        plot_colourmap="viridis",
        special_words="engineering,technology",
        special_colour="green",
        output_file="wordcloud.png"
    )
    print("Workflow completed successfully.")

if __name__ == "__main__":
    main()

# End of file
