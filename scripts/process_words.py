#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
 SCRIPT: Analise scientific words and counts
 AUTHOR: Ricardo Costa
 DATE: October 2025
===========================================================

DESCRIPTION:
------------
This script processes scientific relevant words from public
CVs (ORCID or CienciaVitae) of researchers. It requires as input
a text file containing a list of links to ORCID (https://orcid.org/)
or CienciaVitae (https://www.cienciavitae.pt/).

The process is divided into three steps:

1. Read a text file containing ORCID or CienciaVitae links.
2. Visit each link and scrape the titles of fundings, projects,
   works, outcomes, and journals/conferences.
3. Process and clean the text, lemmatise, filter stopwords, and save
   the most frequent words into a CSV file.

NOTES:
------
- Scraping is performed with Selenium because ORCID/CienciaVitae
  pages may load dynamically and are not fully accessible via
  static HTML parsing.
- Keywords are normalized (lemmatised) and filtered to
  remove common English and Portuguese stopwords, as well as
  domain-generic words.
- To avoid server overload and subsequent client IP blocking,
  a delay is applied between page requests.

OUTPUT:
-------
- CSV file containing the words and their frequencies.

===========================================================
"""

# ================================================
# IMPORT MODULES
# ================================================

import argparse
import re
import time
import csv
import spacy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from spacy.lang.pt.stop_words import STOP_WORDS as STOPWORDS_PT
from spacy.lang.en.stop_words import STOP_WORDS as STOPWORDS_EN

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Analise scientific words counts")
parser.add_argument("--links", required=True, help="Local file with ORCID or CienciaVitae links")
parser.add_argument("--out", default="words.csv", help="Output file (default: words.csv)")
parser.add_argument("--pause", type=int, default=2, help="Delay in seconds between requests (default: 2)")
args = parser.parse_args()

INPUT_LINKS = args.links.strip()
OUTPUT_WORDS = args.out.strip()
PAGE_PAUSE = args.pause

# Additional specific stopwords to be excluded
extra_stopwords = set([
    "research", "profile", "biography", "publications", "works", "university", "student", "education",
    "journal", "conference", "article", "proceeding", "contributor", "international", "nacional", "european", "base",
    "study", "property", "solution", "effect", "approach", "apply", "change", "high", "low",
    "review", "strategy", "self", "case", "load", "center", "centre", "abstract", "path"
])
stopwords = STOPWORDS_PT.union(STOPWORDS_EN).union(extra_stopwords)

# ================================================
# STEP 1: READ CV LINKS
# ================================================

# Read input links
with open(INPUT_LINKS, "r", encoding="utf-8") as f:
    cv_links = [line.strip() for line in f if line]
print(f"Loaded {len(cv_links)} CV links")

# ================================================
# STEP 2: INITIALISE MODULES
# ================================================

# Load spaCy language model for lemmatisation
nlp = spacy.load("en_core_web_sm")

# Configure Selenium options (headless mode for automation)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# ================================================
# STEP 3: SCRAPE CVs
# ================================================

# Dictionary to store word frequencies
words = {}

# Process words in each link
for i, cv_link in enumerate(cv_links, start=1):
    # Check link type
    if "orcid.org" in cv_link:
        cv_type = "orcid"
    elif "cienciavitae.pt" in cv_link:
        cv_type = "cienciavitae"
    else:
        print(f"\033[33m[{i}/{len(cv_links)}] Unknown CV type: {cv_link}CV\033[0m")
        continue
    print(f"[{i}/{len(cv_links)}] Loading {cv_type.upper()}: {cv_link}")
    try:
        driver.get(cv_link)
        time.sleep(PAGE_PAUSE)
    except:
        print(f"\033[33m  Unable to load {cv_type.upper()} CV\033[0m")
        continue

    # Process HTML page
    cv_soup = BeautifulSoup(driver.page_source, "lxml")

    # Array to store extrated text
    text_parts = []

    # ORCID scraping
    if cv_type == "orcid":
        # Extract funding titles
        for h4 in cv_soup.select("h4.funding-title"):
            text_parts.append(h4.get_text(strip=True).replace("\n", " ").strip())
        # Extract work titles
        for h4 in cv_soup.select("h4.work-title"):
            text_parts.append(h4.get_text(strip=True).replace("\n", " ").strip())
        for work in cv_soup.select("app-work"):
            general_data = work.select_one("div.general-data")
            if general_data:
                text_parts.append(general_data.get_text(" ", strip=True).replace("\n", " ").strip())
    # CienciaVitae scraping
    elif cv_type == "cienciavitae":
        # Extract project titles
        for td in cv_soup.select("#proj table td:nth-of-type(2)"):
            text_parts.append(td.get_text(" ", strip=True).replace("\n", " ").strip())
        # Extract production titles
        for li in cv_soup.select("#prod li"):
            # Extract titles between <i>
            title_tag = li.select_one("i")
            if title_tag:
                text_parts.append(title_tag.get_text(strip=True).replace("\n", " ").strip())
            # Extract titles between quotation marks
            text = li.get_text(" ", strip=True).replace("\n", " ")
            match = re.search(r'"(.*?)"', text)
            if match:
                text_parts.append(match.group(1).replace("\n", " ").strip())

    # Combine everything
    text = " ".join(text_parts)

    # Clean text to keep only alphabetic characters and spaces
    text = re.sub(r"[^a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ\s]", " ", text)

    # Lemmatisation and stopword filtering
    doc = nlp(text.lower())
    for token in doc:
        lemma = token.lemma_.strip()
        if len(lemma) > 3 and lemma not in stopwords:
            words[lemma] = words.get(lemma, 0) + 1

# Close Selenium browser
driver.quit()

# ================================================
# STEP 4: SAVE CSV
# ================================================

# Save words and counts to file
with open(OUTPUT_WORDS, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "count"])
    for k, v in sorted(words.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([k, v])
print(f"Words and counts saved at: {OUTPUT_WORDS}")

# End of file
