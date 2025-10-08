#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===============================================================
# ScholarPy - scholarpy-search-links wrapper script
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# ===============================================================
# Description:
# ------------
# Search public scholarly CV links from HTML pages.
# It has two modes of operation:
#
# 1. If argument 'base_url' is set, search institutional profile
#    pages from the provided HTML page(s) (argument 'html_urls') matching the
#    base_url pattern and then visit each institutional profile page
#    to search public scholarly CV links. Useful when the provided HTML
#    page(s) correspond(s) to a list of members, each with a link to
#    an institutional page, where public scholarly CV links are contained.
# 2. If argument 'base_url' is empty, directly search public scholarly CV links
#    inside the provided HTML page(s).
#
# To avoid server overload and subsequent client IP blocking, a delay is
# applied between HTTP/HTTPS requests.
#
# Arguments:
# ----------
# --html_urls   : Input HTML file(s) or URL(s), separated by commas (required).
# --base_url    : Base URL for institutional profile pages (optional, default: none).
# --links_limit : Limit number of links to retrieve (optional, default: 200).
# --page_pause  : Delay in seconds between HTTP/HTTPS requests (optional, default: 3).
# --output_file : Output TXT file containing the found links (optional, default: 'links.txt').
#
# Output:
# -------
# A TXT file containing a list of links is saved to disk.
# ===============================================================

# ===============================================================
# IMPORT MODULES
# ===============================================================

import argparse
from scholarpy.core import search_links

# ===============================================================
# DEFINE FUNCTIONS
# ===============================================================

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Search public scholarly CV links from HTML pages.")
    parser.add_argument("--html_urls", required=True, help="Input HTML file(s) or URL(s), separated by commas (required).")
    parser.add_argument("--base_url", default="", help="Base URL for institutional pages (optional, default: none).")
    parser.add_argument("--links_limit", type=int, default=200, help="Limit number of links to retrieve (optional, default: 200).")
    parser.add_argument("--page_pause", type=int, default=3, help="Delay in seconds between HTTP/HTTPS requests (optional, default: 3).")
    parser.add_argument("--output_file", default="links.txt", help="Output TXT file containing the found CV links (optional, default: `links.txt`).")
    args = parser.parse_args()
    # Call function
    search_links(args.html_urls.strip(), args.base_url.strip(), args.links_limit, args.page_pause, args.output_file.strip())

# ===============================================================
# RUN FUNCTIONS
# ===============================================================

if __name__ == "__main__":
    main()

# End of file
