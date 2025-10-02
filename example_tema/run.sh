#!/bin/bash

# Extract links
python3.9 ../scripts/extract_links.py --html="tema_members.html" --base="https://www.ua.pt/pt/p/" --limit=10;

# Process words
python3.9 ../scripts/process_words.py --links="links.txt";

# Plot word cloud
python3.9 ../scripts/plot_wordcloud.py --words="words.csv" --colormap="viridis" --special="engineering,technology" --highlight="green";

# end of file
