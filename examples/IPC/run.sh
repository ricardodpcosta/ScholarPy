#!/bin/bash

# Extract links
python3.9 ../scripts/extract_links.py --html="https://ipc.uminho.pt/pt-pt/equipa,https://ipc.uminho.pt/pt-pt/equipa?page=2,https://ipc.uminho.pt/pt-pt/equipa?page=3";

# Process words
python3.9 ../scripts/process_words.py --links="links.txt";

# Plot word cloud
python3.9 ../scripts/plot_wordcloud.py --words="words.csv" --colormap="copper" --special="engineering,technology" --highlight="orange";

# end of file
