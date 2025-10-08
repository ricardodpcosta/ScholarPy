#!/bin/bash
# ===============================================================
# ScholarPy - Example usage (Bash)
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# ===============================================================
# Description:
# ------------
# Demonstrates the ScholarPy workflow using CLI commands.
# Assumes ScholarPy is installed via pip and available globally.
#
# Usage:
# ------
# bash example.sh
# ===============================================================

# Step 1: Collect data from public scholarly CVs
scholarpy collect_data \
    --links_file="links.txt" \
    --output_file="data.txt"

# Step 2: Analyse and process words
scholarpy analyse_words \
    --data_file="data.txt" \
    --output_file="words.csv"

# Step 3: Generate wordcloud visualisation
scholarpy plot_wordcloud \
    --words_file="words.csv" \
    --plot_colourmap="viridis" \
    --plot_fontpath=None \
    --plot_maxwords=100 \
    --special_words="analysis,boundary,equation,fluid,flow,mathematical,mechanic" \
    --special_colour="green" \
    --output_file="wordcloud.png"

echo "Workflow completed successfully."

# End of file
