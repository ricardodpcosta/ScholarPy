#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
SCRIPT: Word cloud plotter from words and counts
AUTHOR: Ricardo Costa
DATE: October 2025
===========================================================

DESCRIPTION:
------------
This script plots word clouds from a list of words and associated
counts. It generated two images:

1. A standard word cloud plot containing all words with
   a gradient colour.
2. A recolored version of the same layout, where special
   words are highlighted with a custom colour.

NOTES:
------
- The word layout remains identical between both images to
  allow easy comparison and only the colors differ.

OUTPUT:
-------
- PNG file containing the word cloud plots.

AUTHOR:
-------
Ricardo Costa (rcosta@dep.uminho.pt)

LICENSE:
--------
MIT License (see LICENSE file for details)

REPOSITORY:
-----------
https://github.com/ricardodpcosta/SciWordCloud

DEPENDENCIES:
-------------

USAGE:
------
python plot_wordcloud.py [-h]

===========================================================
"""

# ================================================
# IMPORT MODULES
# ================================================

import argparse
import csv
from wordcloud import WordCloud
import matplotlib
from matplotlib import pyplot as plt

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Word cloud plotter from words and counts")
parser.add_argument("--words", required=True, help="Local CSV file with words and counts")
parser.add_argument("--colormap", default="viridis", help="Word cloud plot colormap (any from Matplotlib, default: viridis)")
parser.add_argument("--special", default="", help="Special words to highlight (default: '')")
parser.add_argument("--highlight", default="green", help="Colour to highlight special words (any from Matplotlib, default: green)")
parser.add_argument("--out", default="wordcloud.png", help="Output file (default: wordcloud.png)")
args = parser.parse_args()

INPUT_WORDS = args.words.strip()
PLOT_COLORMAP = args.colormap.strip()
SPECIAL_WORDS = args.special.strip()
SPECIAL_HIGHLIGHT = args.highlight.strip()
OUTPUT_WORDCLOUD = args.out.strip()

# ================================================
# STEP 1: READ CSV
# ================================================

# Load words and counts from CSV file
words = {}
with open(INPUT_WORDS, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row["word"]
        count = int(row["count"])
        words[word] = count

# Minimum and maximum counts
min_freq = min(words.values())
max_freq = max(words.values())

# ================================================
# STEP 2: GENERATE WORDCLOUD
# ================================================

# Get colormap from Matplotlib
cmap = plt.get_cmap(PLOT_COLORMAP)

# Custom color function to color words according to their size
def gradient_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    # Normalise font size
    norm_size = (words[word] - min_freq) / (max_freq - min_freq)
    norm_size = max(0, min(norm_size, 1))
    r, g, b, _ = cmap(norm_size)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

# Generate the base word cloud plot
wordcloud1 = WordCloud(
    width=1200,
    height=600,
    background_color="white",
    color_func=gradient_color_func,
    max_words=200
).generate_from_frequencies(words)

# Display and save word cloud plot
plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud1, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_WORDCLOUD)
plt.show()
print(f"Word cloud plot saved at: {OUTPUT_WORDCLOUD}")

# IF there are any special words
if SPECIAL_WORDS:
    # Custom color function to highlight certain words
    def special_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        if word in SPECIAL_WORDS:
            return SPECIAL_HIGHLIGHT
        return "gray"
    # Recolor wordcloud1 (keeps the same layout, only changes colors)
    wordcloud2 = wordcloud1.recolor(color_func=special_color_func)

    # Rename output name
    OUTPUT_WORDCLOUD = "special_"+OUTPUT_WORDCLOUD

    # Display and save word cloud plot
    plt.figure(figsize=(15, 7.5))
    plt.imshow(wordcloud2, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(OUTPUT_WORDCLOUD)
    plt.show()
    print(f"Word cloud plot saved at: {OUTPUT_WORDCLOUD}")

# End of file
