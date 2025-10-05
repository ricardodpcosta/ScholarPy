#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
SCRIPT: analise_words.py
AUTHOR: Ricardo Costa
DATE: October 2025
===========================================================

DESCRIPTION:
------------
Analyse relevant scientific words from extracted data.
The process is divided into two steps:

1. Read an input file containing data.
2. Lemmatise, filter and count words.

Words are lemmatised (normalized) and filtered to remove common
English and Portuguese stopwords, as well as domain-generic words.

USAGE:
------
python process_words.py --data <INPUT_DATA_FILE> [--out <OUTPUT_FILE>]

ARGUMENTS:
----------
--data   : Input TXT file containing extracted text (required).
--out    : Output CSV file containing words and their counts (optional, default: `words.csv`).

OUTPUT:
-------
A CSV file with columns `word` and `count`, containing processed and
filtered words.

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
import csv
import spacy
try:
    from spacy.lang.en.stop_words import STOP_WORDS as STOPWORDS_EN
except ImportError as e:
    print("\033[31mEnglish model 'en_core_web_sm' not found\033[0m")
    print("Download it with: python -m spacy download en_core_web_sm")
    sys.exit(1)
try:
    from spacy.lang.pt.stop_words import STOP_WORDS as STOPWORDS_PT
except ImportError as e:
    print("\033[33mPortuguese model 'pt_core_news_sm' not found\033[0m ")
    print("Download it with: python -m spacy download pt_core_news_sm")
    STOPWORDS_PT = set()

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Analyse relevant scientific words from extracted data.")
parser.add_argument("--data", required=True, help="Input TXT file containing extracted text (required).")
parser.add_argument("--out", default="words.csv", help="Output CSV file containing words and their counts (optional, default: `words.csv`).")
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

# Load spaCy language model
try:
    nlp_ = spacy.load("en_core_web_sm")
except OSError:
    print("\033[31mEnglish model 'en_core_web_sm' not found\033[0m")
    print("Download it with: python -m spacy download en_core_web_sm")
    sys.exit(1)

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
