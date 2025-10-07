#!/bin/bash

# Extract links
python3.9 ../scripts/search_links.py --html="https://ipc.uminho.pt/pt-pt/equipa,https://ipc.uminho.pt/pt-pt/equipa?page=2,https://ipc.uminho.pt/pt-pt/equipa?page=3";

# Extract data
python3.9 ../scripts/extract_data.py --links="links.txt"

# Analise words
python3.9 ../scripts/analise_words.py --data="data.txt";

# Plot word cloud
python3.9 ../scripts/plot_wordcloud.py --words="words.csv" --colormap="copper" --special="engineering,technology" --highlight="orange";

# end of file
