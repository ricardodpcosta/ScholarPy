#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
SCRIPT: plot_wordcloud.py
AUTHOR: Ricardo Costa
DATE: October 2025
===========================================================

DESCRIPTION:
------------
Generate word cloud visualisations from word frequency data.
It generated two images:

1. A standard word cloud plot containing all words with
   a gradient colour.
2. A recoloured version of the same layout, where special
   words are highlighted with a custom colour.

The word layout remains identical between both images, allowing for
easy comparison, while only the colours differ.

USAGE:
------
python plot_wordcloud.py --words <INPUT_WORDS_FILE> [--colormap <COLORMAP>]
[--maxwords <MAXWORDS>] [--special <WORDS>] [--highlight <COLOR>] [--out <OUTPUT_FILE>]

ARGUMENTS:
----------

--words       : Input CSV file with words and counts (required).
--colormap    : Matplotlib colourmap for gradient colouring (optional, default: `viridis`).
--maxwords    : Limit number of words to plot (optional, default: 200).
--special     : Comma-separated list of words to highlight in the word cloud (optional, default: none).
--highlight   : Colour to highlight special words (optional, default: `green`).
--out         : Output PNG file containing the word cloud (optional, default: `wordcloud.png`).

OUTPUT:
-------
A PNG image of the generated word cloud. If `--special` is provided,
a second image is generated with highlighted words.

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
import matplotlib
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Generate word cloud visualisations from word frequency data.")
parser.add_argument("--words", required=True, help="Input CSV file with words and counts (required).")
parser.add_argument("--colormap", default="viridis", help="Matplotlib colourmap for gradient colouring (optional, default: `viridis`).")
parser.add_argument("--maxwords", type=int, default=200, help="Limit number of words to plot (optional, default: 200).")
parser.add_argument("--special", default="", help="Comma-separated list of words to highlight in the word cloud (optional, default: none).")
parser.add_argument("--highlight", default="green", help="Colour to highlight special words (optional, default: `green`).")
parser.add_argument("--out", default="wordcloud.png", help="Output PNG file containing the word cloud (optional, default: `wordcloud.png`).")
args = parser.parse_args()

INPUT_WORDS = args.words.strip()
PLOT_COLORMAP = args.colormap.strip()
PLOT_MAXWORDS = args.maxwords
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

# Get colourmap from Matplotlib
cmap = plt.get_cmap(PLOT_COLORMAP)

# Custom colour function to colour words according to their size
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
    max_words=PLOT_MAXWORDS
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
    # Custom colour function to highlight certain words
    def special_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        if word in SPECIAL_WORDS:
            return SPECIAL_HIGHLIGHT
        return "gray"
    # Recolour wordcloud1 (keeps the same layout, only changes colours)
    wordcloud2 = wordcloud1.recolor(color_func=special_color_func)

    # Display and save word cloud plot
    plt.figure(figsize=(15, 7.5))
    plt.imshow(wordcloud2, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("special_"+OUTPUT_WORDCLOUD)
    plt.show()
    print(f"Word cloud plot saved at: special_{OUTPUT_WORDCLOUD}")

# End of file
