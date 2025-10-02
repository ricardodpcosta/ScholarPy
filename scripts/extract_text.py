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
This script performs web scraping from public researcher CVs (ORCID
or CienciaVitae). It requires an input file with links to ORCID
(https://orcid.org/) or CienciaVitae (https://www.cienciavitae.pt/).
The process is divided into three steps:

1. Read an input file containing ORCID or CienciaVitae links.
2. Visit each link and scrape the data on relevant fields, such as titles
   of fundings, projects, works, outcomes, and journals/conferences.
3. Clean and condense the text, keeping only alphabetic characters and spaces
   wihtout repetition.


NOTES:
------
- Scraping is performed with Selenium because ORCID/CienciaVitae
  pages may load dynamically and are not fully accessible via
  static HTML parsing.
- To avoid server overload and subsequent client IP blocking,
  a delay is applied between page requests.

OUTPUT:
-------
- TXT file containing the extracted text.

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
python extract_text.py [-h]

===========================================================
"""

# ================================================
# IMPORT MODULES
# ================================================

import argparse
import re
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Analise scientific words counts")
parser.add_argument("--links", required=True, help="Input file with ORCID or CienciaVitae links")
parser.add_argument("--out", default="text.txt", help="Output file with extracted text (default: text.txt)")
parser.add_argument("--pause", type=int, default=3, help="Delay in seconds between requests (default: 2)")
args = parser.parse_args()

INPUT_LINKS = args.links.strip()
OUTPUT_TEXT = args.out.strip()
PAGE_PAUSE = args.pause

# ================================================
# STEP 1: READ CV LINKS
# ================================================

# Read input links
with open(INPUT_LINKS, "r", encoding="utf-8") as f:
    cv_links = [line.strip() for line in f if line]
if len(cv_links)==1:
    print(f"Loaded {len(cv_links)} link")
else:
    print(f"Loaded {len(cv_links)} links")

# ================================================
# STEP 2: INITIALISE MODULES
# ================================================

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
        print(f"[{i}/{len(cv_links)}] Loading ORCID: {cv_link}")
    elif "cienciavitae.pt" in cv_link:
        cv_type = "cienciavitae"
        print(f"[{i}/{len(cv_links)}] Loading CienciaVitae: {cv_link}")
    else:
        print(f"\033[33m[{i}/{len(cv_links)}] Unknown CV type: {cv_link}CV\033[0m")
        continue
    # Load HTML page
    try:
        driver.get(cv_link)
    except:
        print(f"\033[33m  Unable to load page\033[0m")
        continue
    time.sleep(PAGE_PAUSE)
    # Process HTML page
    cv_soup = BeautifulSoup(driver.page_source, "lxml")
    # Check if page is found
    if cv_type == "orcid":
        title_tag = cv_soup.select_one("title")
        if title_tag and title_tag.get_text(strip=True) != "ORCID":
            user_name = title_tag.get_text(strip=True)
            match = re.match(r"^(.*?)\s*\(", user_name)
            if match:
                user_name = match.group(1).strip()
            else:
                user_name = user_name.strip()
            print(f"\033[32m  Successfully loaded page\033[0m")
        else:
            print(f"\033[33m  Unable to load page, possibly page not found\033[0m")
            continue
    else:
        user_name_tag = cv_soup.select_one("div.user-name")
        if user_name_tag:
            user_name = user_name_tag.get_text(strip=True)
            print(f"\033[32m  Successfully loaded page\033[0m")
        else:
            print(f"\033[33m  Unable to load page, possibly page not found\033[0m")
            continue
    # Array to store extrated text
    text = []
    # ORCID scraping
    if cv_type == "orcid":
        # Extract funding titles
        for h4 in cv_soup.select("h4.funding-title"):
            text.append(h4.find(string=True, recursive=False).replace("\n", " ").strip())
        # Extract work titles
        for h4 in cv_soup.select("h4.work-title"):
            text.append(h4.find(string=True, recursive=False).replace("\n", " ").strip())
        for work in cv_soup.select("app-work"):
            data = work.select_one("div.general-data")
            if data:
                text.append(data.find(string=True, recursive=False).replace("\n", " ").strip())
    # CienciaVitae scraping
    elif cv_type == "cienciavitae":
        # Extract project titles
        for td in cv_soup.select("#proj table td:nth-of-type(2)"):
            text.append(td.find(string=True, recursive=False).replace("\n", " ").strip())
        # Extract production titles
        for li in cv_soup.select("#prod li"):
            # Extract titles between <i>
            title_tag = li.select_one("i")
            if title_tag:
                text.append(title_tag.find(string=True, recursive=False).replace("\n", " ").strip())
            # Extract titles between quotation marks
            string = li.find(string=True, recursive=False).replace("\n", " ").strip()
            match = re.search(r'"(.*?)"', string)
            if match:
                text.append(match.group(1))

# Clean and condense text
for i, string in enumerate(text):
    string = re.sub(r"[^a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ\s]", " ", string)
    string = re.sub(r"\s+", " ", string)
    text[i] = string.strip()

# Close Selenium browser
driver.quit()

# ================================================
# STEP 4: SAVE TXT
# ================================================

# Save text to file
with open(OUTPUT_TEXT, "w", encoding="utf-8") as f:
    f.write("\n".join(text))
print(f"Text saved at: {OUTPUT_TEXT}")

# End of file
