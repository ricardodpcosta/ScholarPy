#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===============================================================
# ScholarPy - scholarpy-plot-wordcloud wrapper script
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# ===============================================================
# Description:
# ------------
# Generate wordcloud visualisations from word frequency data.
# It generates two images:
#
# 1. A standard wordcloud plot containing all words with
#    a gradient colour.
# 2. A recoloured version of the same layout, where special
#    words are coloured with a custom colour.
#
# The word layout remains identical between both images, allowing for
# easy comparison, while only the colours differ.
#
# Usage:
# ------
# Run `scholarpy-plot-wordcloud --help` on the command line.
#
# Arguments:
# ----------
# --words_file      : Input CSV file with words and counts (required).
# --plot_colourmap  : Matplotlib colourmap for gradient colouring (optional, default: 'viridis').
# --plot_maxwords   : Limit number of words to plot (optional, default: 200).
# --special_words   : Comma-separated list of words to highlight in the wordcloud (optional, default: none).
# --special_colour  : Colour to highlight special words (optional, default: 'green').
# --output_file     : Output PNG file containing the wordcloud (optional, default: 'wordcloud.png').
#
# Output:
# -------
# A PNG image of the generated wordcloud is saved to disk. If special words are provided,
# a second image is saved to disk.
# ===============================================================

# ===============================================================
# IMPORT MODULES
# ===============================================================

import argparse
from scholarpy.core import plot_wordcloud

# ===============================================================
# DEFINE FUNCTIONS
# ===============================================================

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate word cloud visualisations from word frequency data.")
    parser.add_argument("--words_file", required=True, help="Input CSV file with words and counts (required).")
    parser.add_argument("--plot_colourmap", default="viridis", help="Matplotlib colourmap for gradient colouring (optional, default: `viridis`).")
    parser.add_argument("--plot_maxwords", type=int, default=200, help="Limit number of words to plot (optional, default: 200).")
    parser.add_argument("--special_words", default="", help="Comma-separated list of words to highlight in the word cloud (optional, default: none).")
    parser.add_argument("--special_colour", default="green", help="Colour to highlight special words (optional, default: `green`).")
    parser.add_argument("--output_file", default="wordcloud.png", help="Output PNG file containing the word cloud (optional, default: `wordcloud.png`).")
    args = parser.parse_args()
    # Call function
    plot_wordcloud(args.words_file.strip(), args.plot_colourmap.strip(), args.plot_maxwords, args.special_words.strip(), args.special_colour.strip(), args.output_file.strip())

# ===============================================================
# RUN FUNCTIONS
# ===============================================================

if __name__ == "__main__":
    main()

# End of file
