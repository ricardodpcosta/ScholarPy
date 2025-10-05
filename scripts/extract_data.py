#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
SCRIPT: extract_data.py
AUTHOR: Ricardo Costa
DATE: October 2025
===========================================================

DESCRIPTION:
------------
Extract relevant textual data from public scholarly CV links.
The process is divided into three steps:

1. Read an input file containing a list of public scholarly CV links.
2. Visit each link and scrape the data on relevant fields, such as titles
   of fundings, projects, works, outcomes, and journals/conferences.
3. Clean and condense the data, keeping only alphabetic characters and spaces
   without repetition.

Scraping is performed with Selenium instead of Requests because some public
scholarly CV pages may load dynamically and are not fully accessible via static
HTML parsing. To avoid server overload and subsequent client IP blocking,
a delay is applied between HTTP/HTTPS requests.

USAGE:
------
python extract_data.py --links <INPUT_LINKS_FILE> [--out <OUTPUT_FILE>]
[--pause <SECONDS>]

ARGUMENTS:
----------
--links  : Input TXT file containing a list of public scholarly CV links (required, one per line).
--pause  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
--out    : Output TXT file containing the extracted textual data (optional, default: `data.txt`).

OUTPUT:
-------
A TXT file containing all extracted text from the profiles, cleaned
and normalised.

AUTHOR:
-------
Ricardo Costa (rcosta@dep.uminho.pt)

LICENSE:
--------
MIT License (see LICENSE file for details)

REPOSITORY:
-----------
https://github.com/ricardodpcosta/SciWordCloud

===========================================================
"""

# ================================================
# IMPORT MODULES
# ================================================

import argparse
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ================================================
# PARSE ARGUMENTS
# ================================================

parser = argparse.ArgumentParser(description="Extract relevant textual data from public scholarly CV links.")
parser.add_argument("--links", required=True, help="Input TXT file containing a list of public scholarly CV links (one per line).")
parser.add_argument("--pause", type=int, default=3, help="Delay in seconds between HTTP/HTTPS requests (optional, default=3).")
parser.add_argument("--out", default="data.txt", help="Output TXT file containing the extracted textual data (optional, default: `data.txt`).")
args = parser.parse_args()

INPUT_LINKS = args.links.strip()
PAGE_PAUSE = args.pause
OUTPUT_DATA = args.out.strip()

# ================================================
# STEP 1: READ LINKS
# ================================================

# Read input links
with open(INPUT_LINKS, "r", encoding="utf-8") as f:
    links = [line.strip() for line in f if line]
if len(links)==1:
    print(f"Loaded {len(links)} link")
else:
    print(f"Loaded {len(links)} links")

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
# STEP 3: SCRAPE PROFILES
# ================================================

# Dictionary to store word frequencies
words = {}

# Process words in each link
for i, link in enumerate(links, start=1):
    # Check link type
    if "orcid.org" in link:
        type = "orcid"
        print(f"[{i}/{len(links)}] Loading ORCID: {link}")
    elif "cienciavitae.pt" in link:
        type = "cienciavitae"
        print(f"[{i}/{len(links)}] Loading CienciaVitae: {link}")
    else:
        print(f"\033[33m[{i}/{len(links)}] Unknown profile type: {link}\033[0m")
        continue
    # Load HTML page
    try:
        driver.get(link)
    except:
        print(f"\033[33m  Unable to load page\033[0m")
        continue
    time.sleep(PAGE_PAUSE)
    # Process HTML page
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Check if page is found
    if type == "orcid":
        title_tag = soup.select_one("title")
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
        user_name_tag = soup.select_one("div.user-name")
        if user_name_tag:
            user_name = user_name_tag.get_text(strip=True)
            print(f"\033[32m  Successfully loaded page\033[0m")
        else:
            print(f"\033[33m  Unable to load page, possibly page not found\033[0m")
            continue
    # Array to store extrated data
    data = []
    # ORCID scraping
    if type == "orcid":
        # Extract funding titles
        for h4 in soup.select("h4.funding-title"):
            data.append(h4.find(string=True, recursive=False).replace("\n", " ").strip())
        # Extract work titles
        for h4 in soup.select("h4.work-title"):
            data.append(h4.find(string=True, recursive=False).replace("\n", " ").strip())
        for work in soup.select("app-work"):
            data = work.select_one("div.general-data")
            if data:
                data.append(data.find(string=True, recursive=False).replace("\n", " ").strip())
    # CienciaVitae scraping
    elif type == "cienciavitae":
        # Extract project titles
        for td in soup.select("#proj table td:nth-of-type(2)"):
            data.append(td.find(string=True, recursive=False).replace("\n", " ").strip())
        # Extract production titles
        for li in soup.select("#prod li"):
            # Extract titles between <i>
            title_tag = li.select_one("i")
            if title_tag:
                data.append(title_tag.find(string=True, recursive=False).replace("\n", " ").strip())
            # Extract titles between quotation marks
            string = li.find(string=True, recursive=False).replace("\n", " ").strip()
            match = re.search(r'"(.*?)"', string)
            if match:
                data.append(match.group(1))

# Clean and condense data
for i, string in enumerate(data):
    string = re.sub(r"[^a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ\s]", " ", string)
    string = re.sub(r"\s+", " ", string)
    data[i] = string.strip()

# Close Selenium browser
driver.quit()

# ================================================
# STEP 4: SAVE DATA
# ================================================

# Save data to file
with open(OUTPUT_DATA, "w", encoding="utf-8") as f:
    f.write("\n".join(data))
print(f"Data saved at: {OUTPUT_DATA}")

# End of file
