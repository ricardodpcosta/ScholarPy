#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================
ScholarPy - Unified command-line interface
===============================================================
Author: Ricardo Costa (rcosta@dep.uminho.pt)
License: MIT License (see LICENSE file for details)
Repository: https://github.com/ricardodpcosta/ScholarPy
===============================================================
Description:
------------
Unified command-line interface for ScholarPy. Supports the following
tools:

1. search_links    - Search public scholarly CV links.
2. collect_data    - Collect textual data from links.
3. analyse_words   - Analyse relevant word frequencies.
4. plot_wordcloud  - Generate wordcloud visualisations.

Usage:
------
scholarpy [--help] {search_links,collect_data,analyse_words,plot_wordcloud} ...

Arguments:
----------
--help        : Shows this help message and exits.

Output:
-------
A file is saved to disk depending of the executed tool.
===============================================================
"""

# ===============================================================
# IMPORT MODULES
# ===============================================================

import argparse
from scholarpy.core import search_links, collect_data, analyse_words, plot_wordcloud

# ===============================================================
# SCHOLARPY
# ===============================================================

def main():
    parser = argparse.ArgumentParser(description="ScholarPy unified command-line interface.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to run")

    # search_links
    parser_links = subparsers.add_parser("search_links", help="Search public scholarly CV links from HTML pages.")
    parser_links.add_argument("--html_urls", required=True, help="Input HTML file(s) or URL(s), separated by commas (required).")
    parser_links.add_argument("--base_url", default="", help="Base URL for institutional pages (optional, default: None).")
    parser_links.add_argument("--links_limit", type=int, default=200, help="Limit number of links to retrieve (optional, default: 200).")
    parser_links.add_argument("--page_pause", type=int, default=3, help="Delay in seconds between HTTP/HTTPS requests (optional, default: 3).")
    parser_links.add_argument("--output_file", default="links.txt", help="Output TXT file containing the found CV links (optional, default: `links.txt`).")

    # collect_data
    parser_collect = subparsers.add_parser("collect_data", help="Collect relevant textual data from public scholarly CV links.")
    parser_collect.add_argument("--links_file", required=True, help="Input TXT file containing a list of public scholarly CV links (required).")
    parser_collect.add_argument("--page_pause", type=int, default=3, help="Delay in seconds between HTTP/HTTPS requests (optional, default: 3).")
    parser_collect.add_argument("--output_file", default="data.txt", help="Output TXT file containing the collected data (optional, default: `data.txt`).")

    # analyse_words
    parser_analyse = subparsers.add_parser("analyse_words", help="Analyse relevant scientific words from collected data.")
    parser_analyse.add_argument("--data_file", required=True, help="Input TXT file containing collected text (required).")
    parser_analyse.add_argument("--output_file", default="words.csv", help="Output CSV file containing words and their counts (optional, default: `words.csv`).")

    # plot_wordcloud
    parser_wordcloud = subparsers.add_parser("plot_wordcloud", help="Generate wordcloud visualisations from word frequency data.")
    parser_wordcloud.add_argument("--words_file", required=True, help="Input CSV file with words and counts (required).")
    parser_wordcloud.add_argument("--plot_colourmap", default="viridis", help="Matplotlib colourmap for gradient colouring (optional, default: `viridis`).")
    parser_wordcloud.add_argument("--plot_fontpath", default=None, help="Path to TTF font file (optional, default: None).")
    parser_wordcloud.add_argument("--plot_maxwords", type=int, default=200, help="Limit number of words to plot (optional, default: 200).")
    parser_wordcloud.add_argument("--special_words", default=None, help="Comma-separated list of words to highlight in the wordcloud (optional, default: None).")
    parser_wordcloud.add_argument("--special_colour", default="green", help="Colour to highlight special words (optional, default: `green`).")
    parser_wordcloud.add_argument("--output_file", default="wordcloud.png", help="Output PNG file containing the wordcloud (optional, default: `wordcloud.png`).")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "search_links":
        search_links(
            html_urls=args.html_urls.strip(),
            base_url=args.base_url.strip(),
            links_limit=args.links_limit,
            page_pause=args.page_pause,
            output_file=args.output_file.strip()
        )
    elif args.command == "collect_data":
        collect_data(
            links_file=args.links_file.strip(),
            page_pause=args.page_pause,
            output_file=args.output_file.strip()
        )
    elif args.command == "analyse_words":
        analyse_words(
            data_file=args.data_file.strip(),
            output_file=args.output_file.strip()
        )
    elif args.command == "plot_wordcloud":
        plot_wordcloud(
            words_file=args.words_file.strip(),
            plot_colourmap=args.plot_colourmap.strip(),
            plot_maxwords=args.plot_maxwords,
            special_words=args.special_words.strip(),
            special_colour=args.special_colour.strip(),
            output_file=args.output_file.strip()
        )
    else:
        parser.print_help()

# ===============================================================
# RUN FUNCTION
# ===============================================================

if __name__ == "__main__":
    main()

# End of file
