#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
SCRIPT: Search ORCID and CienciaVitae links
AUTHOR: Ricardo Costa
DATE: October 2025
===========================================================

DESCRIPTION:
------------
This script searches ORCID or CienciaVitae links from HTML pages.
Requires a input HTML file or URL. It has two modes of operation:

1. If BASE_URL (option --base) is set, search researcher profile
   links from the provided HTML page(s) (option --html) matching the
   BASE_URL pattern and then visit each researcher profile page
   to search ORCID/CienciaVitae links. Useful when the provided HTML
   page(s) correspond(s) to a list of researchers with links to
   individual pages, where ORCID/CienciaVitae links are contained.
2. If BASE_URL is empty, directly search ORCID/CienciaVitae links
   inside the provided HTML page(s).

ARGUMENTS:
----------
--html   : Input HTML file(s) or URL(s), separated by commas
--base   : Base URL for individual pages (leave empty for direct mode)
--out    : Output file with ORCID/CienciaVitae links
--limit  : Limit number of links to search (default=200)
--pause  : Delay in seconds after loading each page (default=3)

OUTPUT:
-------
- TXT file containing the list of CV links (ORCID or CienciaVitae).
  Each line contains the format: <type>|<url>

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
python search_links.py [-h]

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

parser = argparse.ArgumentParser(description="Search ORCID and CienciaVitae links")
parser.add_argument("--html", required=True, help="Input HMTL file(s) or URL(s), separated by commas")
parser.add_argument("--base", default="", help="Base URL for researcher profile pages (empty for direct mode)")
parser.add_argument("--out", default="links.txt", help="Output file with links (default: links.txt)")
parser.add_argument("--limit", type=int, default=200, help="Limit number of links to search (default: 200)")
parser.add_argument("--pause", type=int, default=3, help="Delay in seconds between requests (default: 3)")
args = parser.parse_args()

HTML_SOURCES = args.html.strip()
BASE_URL = args.base.strip()
OUTPUT_LINKS = args.out.strip()
TEAM_LIMIT = args.limit
PAGE_PAUSE = args.pause

# ================================================
# STEP 1: INITIALISE MODULES
# ================================================

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# ================================================
# STEP 2: PROCESS EACH SOURCE
# ================================================

# Array storing CV links
cv_links = []

# Split multiple sources
sources = [src.strip() for src in HTML_SOURCES.split(",") if src.strip()]

# Search links in each source
for source in sources:
    # Limit number of links
    if len(cv_links)==TEAM_LIMIT:
        break
    print(f"Processing source: {source}")
    # Load HTML (remote or local)
    if source.startswith("http://") or source.startswith("https://"):
        try:
            driver.get(source)
            time.sleep(PAGE_PAUSE)
            html = driver.page_source
        except:
            print(f"\033[33m  Unable to load page\033[0m")
            continue
    else:
        try:
            with open(source, "r", encoding="utf-8") as f:
                html = f.read()
        except:
            print(f"\033[33m  Unable to load page\033[0m")
            continue
    # Process HTML page
    soup = BeautifulSoup(html, "lxml")
    # Search links on personal pages
    if BASE_URL:
        pattern = re.compile(rf"^{BASE_URL}")
        profile_links = [a["href"] for a in soup.find_all("a", href=pattern)]
        print(f"  Found {len(profile_links)} researcher profile pages")

        # Load researcher profile
        for i, link in enumerate(profile_links, start=1):
            print(f"[{i}/{len(profile_links)}] Loading profile: {link}")
            try:
                driver.get(link)
                time.sleep(PAGE_PAUSE)
            except:
                print(f"\033[33m  Unable to load page\033[0m")
                continue
            # Process HTML page
            bs_soup = BeautifulSoup(driver.page_source, "lxml")
            # Try ORCID first
            orcid_tag = bs_soup.find("a", href=lambda x: x and "orcid.org" in x)
            if orcid_tag:
                cv_links.append(f"{orcid_tag['href']}")
                print(f"\033[32m  ORCID found: {orcid_tag['href']}\033[0m")
                # Limit number of links
                if len(cv_links)==TEAM_LIMIT:
                    break
            # Try CienciaVitae otherwise
            else:
                cienciavitae_tag = bs_soup.find("a", href=lambda x: x and "cienciavitae.pt" in x)
                if cienciavitae_tag:
                    cv_links.append(f"{cienciavitae_tag['href']}")
                    print(f"\033[32m  CienciaVitae found: {cienciavitae_tag['href']}\033[0m")
                    # Limit number of links
                    if len(cv_links)==TEAM_LIMIT:
                        break
                else:
                    print("\033[33m  No ORCID or CienciaVitae found\033[0m")
    # Search links directly in HTML
    else:
        # Try ORCID first
        orcid_tags = soup.find_all("a", href=lambda x: x and "orcid.org" in x)
        if orcid_tags:
            for tag in orcid_tags:
                cv_links.append(f"{tag['href']}")
                print(f"\033[32m  ORCID found: {tag['href']}\033[0m")
                # Limit number of links
                if len(cv_links)==TEAM_LIMIT:
                    break
        # Try CienciaVitae otherwise
        else:
            cienciavitae_tags = soup.find_all("a", href=lambda x: x and "cienciavitae.pt" in x)
            for tag in cienciavitae_tags:
                cv_links.append(f"{tag['href']}")
                print(f"\033[32m  CienciaVitae found: {tag['href']}\033[0m")
                # Limit number of links
                if len(cv_links)==TEAM_LIMIT:
                    break

# Close driver
driver.quit()

# ================================================
# STEP 3: SAVE LINKS
# ================================================

# Save links to file
with open(OUTPUT_LINKS, "w", encoding="utf-8") as f:
    for line in cv_links:
        f.write(line + "\n")
print(f"Links saved at: {OUTPUT_LINKS}")

# End of file
