#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================================
 SCRIPT: Extract ORCID and CienciaVitae links
 AUTHOR: Ricardo Costa
 DATE: October 2025
===========================================================

DESCRIPTION:
------------
This script extracts ORCID or CienciaVitae links from HTML pages.
or from researchers' personal pages or directly from the team page.

Two modes of operation:

1. If BASE_URL (option --base) is set, extract researcher profile
   links from the provided HTML page(s) (option --html) matching the
   BASE_URL pattern and then visit each researcher profile page
   to extract ORCID/CienciaVitae links. Useful when the provided HTML
   page(s) correspond(s) to a list of researchers with links to
   individual pages, where ORCID/CienciaVitae links are contained.
2. If BASE_URL is empty, directly search ORCID/CienciaVitae links
   inside the provided HTML page(s).

ARGUMENTS:
----------
--html   : Local HTML file(s) or URL(s), separated by commas
--base   : Base URL for individual pages (leave empty for direct mode)
--out    : Output file with ORCID/CienciaVitae links
--limit  : Limit number of researchers to analyse (default=50)
--pause  : Delay in seconds after loading each page (default=2)

OUTPUT:
-------
- TXT file containing the list of CV links (ORCID or CienciaVitae).
  Each line contains the format: <type>|<url>

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

parser = argparse.ArgumentParser(description="Extract ORCID and CienciaVitae links")
parser.add_argument("--html", required=True, help="Local file(s) or URL(s), separated by commas")
parser.add_argument("--base", default="", help="Base URL for researcher profile pages (empty for direct mode)")
parser.add_argument("--out", default="links.txt", help="Output file (default: links.txt)")
parser.add_argument("--limit", type=int, default=50, help="Limit number of researchers (default: 50)")
parser.add_argument("--pause", type=int, default=2, help="Delay in seconds between requests (default: 2)")
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
    print(f"Processing source: {source}")

    # Load HTML (remote or local)
    if source.startswith("http://") or source.startswith("https://"):
        try:
            driver.get(source)
            time.sleep(PAGE_PAUSE)
            html = driver.page_source
        except:
            print(f"\033[33m  Could not load URL: {source}\033[0m")
            continue
    else:
        try:
            with open(source, "r", encoding="utf-8") as f:
                html = f.read()
        except:
            print(f"\033[33m  Could not open local file: {source}\033[0m")
            continue

    # Process HTML page
    soup = BeautifulSoup(html, "lxml")

    if BASE_URL:
        # Search links on researcher profile pages
        pattern = re.compile(rf"^{BASE_URL}")
        profile_links = [a["href"] for a in soup.find_all("a", href=pattern)]

        # Limit number of researchers
        if TEAM_LIMIT:
            profile_links = profile_links[:TEAM_LIMIT]
        print(f"  Found {len(profile_links)} researcher profile pages")

        # Load researcher profile
        for i, link in enumerate(profile_links, start=1):
            print(f"[{i}/{len(profile_links)}] Loading profile: {link}")
            try:
                driver.get(link)
                time.sleep(PAGE_PAUSE)
            except:
                print(f"\033[33m  Could not load: {link}\033[0m")
                continue

            # Process HTML page
            bs_soup = BeautifulSoup(driver.page_source, "lxml")

            # Try ORCID first
            orcid_tag = bs_soup.find("a", href=lambda x: x and "orcid.org" in x)
            if orcid_tag:
                cv_links.append(f"{orcid_tag['href']}")
                print(f"\033[32m  ORCID found: {orcid_tag['href']}\033[0m")
                continue
            else:
                # Try CienciaVitae otherwise
                cienciavitae_tag = bs_soup.find("a", href=lambda x: x and "cienciavitae.pt" in x)
                if cienciavitae_tag:
                    cv_links.append(f"{cienciavitae_tag['href']}")
                    print(f"\033[32m  CienciaVitae found: {cienciavitae_tag['href']}\033[0m")
                else:
                    print("\033[33m  No ORCID or CienciaVitae found\033[0m")

    else:
        # Search links directly in HTML
        orcid_tags = soup.find_all("a", href=lambda x: x and "orcid.org" in x)
        cienciavitae_tags = soup.find_all("a", href=lambda x: x and "cienciavitae.pt" in x)

        # ORCID links
        for tag in orcid_tags:
            cv_links.append(f"{tag['href']}")
            print(f"\033[32m  ORCID found: {tag['href']}\033[0m")

        # CienciaVitae links
        for tag in cienciavitae_tags:
            cv_links.append(f"{tag['href']}")
            print(f"\033[32m  CienciaVitae found: {tag['href']}\033[0m")

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
