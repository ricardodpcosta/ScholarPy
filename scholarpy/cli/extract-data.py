#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================
ScholarPy - extract-data command line interface
===============================================================
Author: Ricardo Costa (rcosta@dep.uminho.pt)
License: MIT License (see LICENSE file for details)
Repository: https://github.com/ricardodpcosta/ScholarPy
===============================================================
Description:
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

Arguments:
----------
--links_file  : Input TXT file containing a list of public scholarly CV links (required).
--page_pause  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
--output_file : Output TXT file containing the extracted data (optional, default: 'data.txt').

Output:
-------
A TXT file containing all extracted text from the public scholarly CV links
is saved to disk.
===============================================================
"""

# ================================================
# IMPORT MODULES
# ================================================

import argparse
from scholarpy.core import extract_data

# ================================================
# DEFINE FUNCTIONS
# ================================================

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Extract relevant textual data from public scholarly CV links.")
    parser.add_argument("--links_file", required=True, help="Input TXT file containing a list of public scholarly CV links (required).")
    parser.add_argument("--page_pause", type=int, default=3, help="Delay in seconds between HTTP/HTTPS requests (optional, default: 3).")
    parser.add_argument("--output_file", default="data.txt", help="Output TXT file containing the extracted data (optional, default: `data.txt`).")
    args = parser.parse_args()
    # Call function
    extract_data(args.links_file.strip(), args.page_pause, args.output_file.strip())

# ================================================
# RUN FUNCTIONS
# ================================================

if __name__ == "__main__":
    main()

# End of file
