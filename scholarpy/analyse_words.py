#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================
ScholarPy - analyse-words wrapper script
===============================================================
Author: Ricardo Costa (rcosta@dep.uminho.pt)
License: MIT License (see LICENSE file for details)
Repository: https://github.com/ricardodpcosta/ScholarPy
===============================================================
Description:
------------
Analyse relevant scientific words from extracted data.
The process is divided into two steps:

1. Read an input file containing data.
2. Lemmatise, filter, and count words.

Words are lemmatised (normalized) and filtered to remove common
English and Portuguese stopwords, as well as domain-generic words.

Arguments:
----------
--data_file   : Input TXT file containing extracted text (required).
--output_file : Output CSV file containing words and their counts (optional, default: 'words.csv').

Output:
-------
A CSV file with words and counts is saved to disk.
===============================================================
"""

# ===============================================================
# IMPORT MODULES
# ===============================================================

import argparse
from scholarpy.core import analyse_words

# ===============================================================
# DEFINE FUNCTIONS
# ===============================================================

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Analyse relevant scientific words from extracted data.")
    parser.add_argument("--data_file", required=True, help="Input TXT file containing extracted text (required).")
    parser.add_argument("--output_file", default="words.csv", help="Output CSV file containing words and their counts (optional, default: `words.csv`).")
    args = parser.parse_args()
    # Call function
    extract_data(args.data_file.strip(), args.output_file.strip())

# ===============================================================
# RUN FUNCTIONS
# ===============================================================

if __name__ == "__main__":
    main()

# End of file
