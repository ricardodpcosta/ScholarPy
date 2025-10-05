#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
SCRIPT: Analise words from data
AUTHOR: Ricardo Costa
DATE: October 2025
===========================================================

DESCRIPTION:
------------
This script analises relevant scientific words from extracted data.
It requires an input file data. The process is divided into
two steps:

1. Read an input file containing data.
2. Lemmatise, filter and count words.

NOTES:
------
- Words are lemmatised (normalized) and filtered to
  remove common English and Portuguese stopwords, as well as
  domain-generic words.

OUTPUT:
-------
- CSV file containing the processed words.

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
python process_words.py [-h]

===========================================================
"""

# ================================================
# IMPORT MODULES
# ================================================

import argparse
import re
import time
import csv
from bs4 import BeautifulSoup
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS as STOPWORDS_PT
from spacy.lang.en.stop_words import STOP_WORDS as STOPWORDS_EN

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Analise scientific words counts")
parser.add_argument("--data", required=True, help="Input file with data to analise")
parser.add_argument("--out", default="words.csv", help="Output file with processed words (default: words.csv)")
args = parser.parse_args()

INPUT_DATA = args.data.strip()
OUTPUT_WORDS = args.out.strip()

# Additional specific stopwords to be excluded
extra_stopwords = set([
    "abstract", "académico", "academic", "acta", "anual", "approach", "apply", "artigo", "article",
    "base", "case", "center", "centre", "centro", "change", "congresso", "conference", "contributor",
    "decrease", "education", "effect", "estrangeiro", "european", "europeu", "high", "increase", "portuguesa", "portuguese",
    "instituição", "instituto", "internacional", "international", "journal", "jornal", "load", "low", "report",
    "national", "nacional", "path", "portugal", "proceeding", "profile", "property", "publications",
    "reduce", "research", "review", "self", "simpósio", "study", "strategy", "student", "symposium",
    "tipo", "university", "universidade", "user", "works", "workshop"
])
stopwords = STOPWORDS_PT.union(STOPWORDS_EN).union(extra_stopwords)

# ================================================
# STEP 1: READ DATA
# ================================================

# Read data
with open(INPUT_DATA, "r", encoding="utf-8") as f:
    data = f.read()

# ================================================
# STEP 2: INITIALISE MODULES
# ================================================

# Load spaCy language model for lemmatisation
nlp = spacy.load("en_core_web_sm")

# ================================================
# STEP 3: ANALISE DATA
# ================================================

# Dictionary to store word frequencies
words = {}

# Lemmatisation and stopword filtering
doc = nlp(data.lower())
for token in doc:
    lemma = token.lemma_.strip()
    if len(lemma) > 3 and lemma not in stopwords:
        words[lemma] = words.get(lemma, 0) + 1

# ================================================
# STEP 4: SAVE WORDS
# ================================================

# Save words and counts to file
with open(OUTPUT_WORDS, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "count"])
    for k, v in sorted(words.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([k, v])
print(f"Words and counts saved at: {OUTPUT_WORDS}")

# End of file
