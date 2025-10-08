# ===============================================================
# ScholarPy - Core module
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# Description: Core functionalities for ScholarPy.
# ===============================================================

# ===============================================================
# IMPORT MODULES
# ===============================================================

import os, sys, re, time, csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
import spacy
try:
    from spacy.lang.en.stop_words import STOP_WORDS as STOPWORDS_EN
except ImportError as e:
    print("\033[31mEnglish model 'en_core_web_lg' not found: {e}\033[0m")
    print("Download it with: python -m spacy download en_core_web_lg")
    sys.exit(1)
try:
    from spacy.lang.pt.stop_words import STOP_WORDS as STOPWORDS_PT
except ImportError as e:
    print("\033[33mPortuguese model 'pt_core_news_lg' not found: {e}\033[0m")
    print("Download it with: python -m spacy download pt_core_news_lg")
    STOPWORDS_PT = set()
# from spacy.tokenizer import Tokenizer
# from spacy.util import compile_infix_regex
import matplotlib
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from .globals import *

# ===============================================================
# GLOBAL VARIABLES
# ===============================================================

STOPWORDS_PT = locals().get("STOPWORDS_PT", set())
STOPWORDS_EN = locals().get("STOPWORDS_EN", set())
STOPWORDS = STOPWORDS_PT.union(STOPWORDS_EN).union(STOPWORDS)

# ANSI COLOUR ESCAPE CODES
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

# ===============================================================
# HELPER FUNCTIONS
# ===============================================================

def print_info(message):
    """Prints an info message in default."""
    print(f"{message}")

def print_success(message):
    """Prints a success message in green."""
    print(f"{GREEN}{message}{RESET}")

def print_warning(message):
    """Prints a warning message in yellow."""
    print(f"{YELLOW}{message}{RESET}")

def print_error(message):
    """Prints an error message in red."""
    print(f"{RED}{message}{RESET}")

def translate_en(text):
    """Translate text to English."""
    # Empty string
    text = text.strip()
    if not text:
        return ""
    # Skip very short or non-alphabetic strings
    if len(text) < 3 or not any(c.isalpha() for c in text):
        return text
    # Translate text
    try:
        lang = detect(text)
        if lang != "en":
            text = GoogleTranslator(source="auto", target="en").translate(text)
    except LangDetectException:
        # Could not detect language
        return text
    except Exception:
        # Catch unexpected translation API errors
        return text
    return text

if __name__ == "__main__":
    print_warning("This module is intended to be imported, not run directly")

# ===============================================================
# SEARCH LINKS
# ===============================================================

def search_links(html_urls, base_url=None, links_limit=200, page_pause=3, output_file="links.txt"):
    """
    Description:
    ------------
    Search public scholarly CV links from HTML pages.
    It has two modes of operation:

    1. If argument 'base_url' is set, search institutional profile
       pages from the provided HTML page(s) (argument 'html_urls') matching the
       base_url pattern and then visit each institutional profile page
       to search public scholarly CV links. Useful when the provided HTML
       page(s) correspond(s) to a list of members, each with a link to
       an institutional page, where public scholarly CV links are contained.
    2. If argument 'base_url' is empty, directly search public scholarly CV links
       inside the provided HTML page(s).

    To avoid server overload and subsequent client IP blocking, a delay is
    applied between HTTP/HTTPS requests.

    Arguments:
    ----------
    html_urls   : Input HTML file(s) or URL(s), separated by commas (required).
    base_url    : Base URL for institutional profile pages (optional, default: None).
    links_limit : Limit number of links to retrieve (optional, default: 200).
    page_pause  : Delay in seconds between HTTP/HTTPS requests (optional, default: 3).
    output_file : Output TXT file containing the found links (optional, default: 'links.txt').

    Returns:
    --------
    None.

    Output:
    -------
    A TXT file containing a list of links is saved to disk.
    """
    # STEP 1: INITIALISE WEB DRIVER
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    # STEP 2: PROCESS EACH HTML
    # Array storing links
    links = []
    # Split multiple htmls
    html_urls = [src.strip() for src in html_urls.split(",") if src.strip()]
    # Search links in each html
    for html_url in html_urls:
        # Limit number of links
        if len(links)==links_limit:
            break
        print_info(f"Processing HTML: {html_url}")
        # Read HTML
        if html_url.startswith("http://") or html_url.startswith("https://"):
            try:
                driver.get(html_url)
                time.sleep(page_pause)
                html = driver.page_source
            except Exception as e:
                print_info(f"Unable to load page: {e}")
                continue
        else:
            try:
                if not os.path.exists(html_url):
                    print_error(f"Input file not found: {html_url}")
                    return
                with open(html_url, "r", encoding="utf-8") as f:
                    html = f.read()
            except Exception as e:
                print_warning(f"  Unable to load page: {e}")
                continue
        # Process HTML page
        soup = BeautifulSoup(html, "lxml")
        # Search links on personal pages
        if base_url:
            pattern = re.compile(rf"^{base_url}")
            profile_links = [a["href"] for a in soup.find_all("a", href=pattern)]
            print_info(f"  Found {len(profile_links)} institutional profile pages")
            # Load institutional profile
            for i, link in enumerate(profile_links, start=1):
                print_info(f"[{i}/{len(profile_links)}] Loading profile: {link}")
                try:
                    driver.get(link)
                    time.sleep(page_pause)
                except Exception as e:
                    print_warning(f"  Unable to load page: {e}")
                    continue
                # Process HTML page
                bs_soup = BeautifulSoup(driver.page_source, "lxml")
                # Try ORCID first
                orcid_tag = bs_soup.find("a", href=lambda x: x and "orcid.org" in x)
                if orcid_tag:
                    links.append(f"{orcid_tag['href']}")
                    print_success(f"  ORCID found: {orcid_tag['href']}")
                    # Limit number of links
                    if len(links)==links_limit:
                        break
                # Try CienciaVitae otherwise
                else:
                    cienciavitae_tag = bs_soup.find("a", href=lambda x: x and "cienciavitae.pt" in x)
                    if cienciavitae_tag:
                        links.append(f"{cienciavitae_tag['href']}")
                        print_success(f"  CienciaVitae found: {cienciavitae_tag['href']}")
                        # Limit number of links
                        if len(links)==links_limit:
                            break
                    else:
                        print_warning(f"  No ORCID or CienciaVitae found")
        # Search links directly in HTML
        else:
            # Try ORCID first
            orcid_tags = soup.find_all("a", href=lambda x: x and "orcid.org" in x)
            if orcid_tags:
                for tag in orcid_tags:
                    links.append(f"{tag['href']}")
                    print_success(f"  ORCID found: {tag['href']}")
                    # Limit number of links
                    if len(links)==links_limit:
                        break
            # Try CienciaVitae otherwise
            else:
                cienciavitae_tags = soup.find_all("a", href=lambda x: x and "cienciavitae.pt" in x)
                for tag in cienciavitae_tags:
                    links.append(f"{tag['href']}")
                    print_success(f"  CienciaVitae found: {tag['href']}")
                    # Limit number of links
                    if len(links)==links_limit:
                        break
    # Close driver
    driver.quit()
    # STEP 3: SAVE LINKS
    # Save links to file
    with open(output_file, "w", encoding="utf-8") as f:
        for line in links:
            f.write(line + "\n")
    print_info(f"Links file saved at: {output_file}")

# ===============================================================
# COLLECT DATA
# ===============================================================

def collect_data(links_file, page_pause=3, output_file="data.txt"):
    """
    Description:
    ------------
    Collect relevant textual data from public scholarly CV links.
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
    links_file  : Input TXT file containing a list of public scholarly CV links (required).
    page_pause  : Delay in seconds between HTTP/HTTPS requests (optional, default=3).
    output_file : Output TXT file containing the collected data (optional, default: 'data.txt').

    Returns:
    --------
    None.

    Output:
    -------
    A TXT file containing all collected text from the public scholarly CV links
    is saved to disk.
    """
    # STEP 1: READ LINKS
    # Read links
    if not os.path.exists(links_file):
        print_error(f"Input file not found: {links_file}")
        return
    with open(links_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line]
    if len(links)==1:
        print_info(f"Loaded {len(links)} link")
    else:
        print_info(f"Loaded {len(links)} links")
    # STEP 2: INITIALISE MODULES
    # Configure Selenium options (headless mode for automation)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    # STEP 3: SCRAPE PROFILES
    # Array to store extrated data
    data = []
    # Collect text from each link
    for i, link in enumerate(links, start=1):
        # Check link type
        if "orcid.org" in link:
            link_type = "orcid"
            print_info(f"[{i}/{len(links)}] Loading ORCID: {link}")
        elif "cienciavitae.pt" in link:
            link_type = "cienciavitae"
            print_info(f"[{i}/{len(links)}] Loading CienciaVitae: {link}")
        else:
            print_warning(f"[{i}/{len(links)}] Unknown profile type: {link}")
            continue
        # Load HTML page
        try:
            driver.get(link)
        except Exception as e:
            print_warning(f"  Unable to load page: {e}")
            continue
        time.sleep(page_pause)
        # Process HTML page
        soup = BeautifulSoup(driver.page_source, "lxml")
        # Check if page is found
        if link_type == "orcid":
            title_tag = soup.select_one("title")
            if title_tag and title_tag.get_text(strip=True) != "ORCID":
                user_name = title_tag.get_text(strip=True)
                match = re.match(r"^(.*?)\s*\(", user_name)
                if match:
                    user_name = match.group(1).strip()
                else:
                    user_name = user_name.strip()
                print_success(f"  Successfully loaded page")
            else:
                print_warning(f"  Unable to load page, possibly page not found")
                continue
        else:
            user_name_tag = soup.select_one("div.user-name")
            if user_name_tag:
                user_name = user_name_tag.get_text(strip=True)
                print_success(f"  Successfully loaded page")
            else:
                print_warning(f"  Unable to load page, possibly page not found")
                continue
        # ORCID scraping
        if link_type == "orcid":
            # Collect funding titles
            for h4 in soup.select("h4.funding-title"):
                text = h4.find(string=True, recursive=False).replace("\n", " ")
                if text:
                    data.append(translate_en(text))
            # Collect work titles
            for h4 in soup.select("h4.work-title"):
                text = h4.find(string=True, recursive=False).replace("\n", " ")
                if text:
                    data.append(translate_en(text))
            for work in soup.select("app-work"):
                data_tag = work.select_one("div.general-data")
                if data_tag:
                    text = data_tag.find(string=True, recursive=False).replace("\n", " ")
                    if text:
                        data.append(translate_en(text))
        # CienciaVitae scraping
        elif link_type == "cienciavitae":
            # Collect project titles
            for td in soup.select("#proj table td:nth-of-type(2)"):
                text = td.find(string=True, recursive=False).replace("\n", " ")
                if text:
                    data.append(translate_en(text))
            # Collect production titles
            for li in soup.select("#prod li"):
                # Collect titles between <i>
                title_tag = li.select_one("i")
                if title_tag:
                    text = title_tag.find(string=True, recursive=False).replace("\n", " ")
                    if text:
                        data.append(translate_en(text))
                # Collect titles between quotation marks
                string = li.find(string=True, recursive=False).replace("\n", " ")
                match = re.search(r'"(.*?)"', string)
                if match:
                    text = match.group(1)
                    if text:
                        data.append(translate_en(text))
    # Close driver
    driver.quit()
    # Clean and condense data
    for i, string in enumerate(data):
        string = re.sub(r"[^a-zA-ZáéíóúàãõâêîôûçÁÉÍÓÚÀÃÕÂÊÎÔÛÇ\s]", " ", string)
        string = re.sub(r"\s+", " ", string)
        data[i] = string.lower().strip()
    # STEP 4: SAVE DATA
    # Save data to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(data))
    print_info(f"Data file saved at: {output_file}")

# ===============================================================
# ANALISE WORDS
# ===============================================================

def analyse_words(data_file, output_file="words.txt"):
    """
    Description:
    ------------
    Analyse relevant scientific words from collected data.
    The process is divided into two steps:

    1. Read an input file containing data.
    2. Lemmatise, filter, and count words.

    Words are lemmatised (normalized) and filtered to remove common
    English and Portuguese stopwords, as well as domain-generic words.

    Arguments:
    ----------
    data_file   : Input TXT file containing collected text (required).
    output_file : Output CSV file containing words and their counts (optional, default: 'words.csv').

    Returns:
    --------
    None.

    Output:
    -------
    A CSV file with words and counts is saved to disk.
    """
    # STEP 1: READ DATA
    # Read data
    if not os.path.exists(data_file):
        print_error(f"Input file not found: {data_file}")
        return
    with open(data_file, "r", encoding="utf-8") as f:
        data = f.read()
    # STEP 2: INITIALISE MODULES
    # Load spaCy language model
    try:
        nlp = spacy.load("en_core_web_lg")
    except OSError:
        print_error("English model 'en_core_web_lg' not found")
        print_info("Download it with: python -m spacy download en_core_web_lg")
        sys.exit(1)
    # # Customize tokenizer to preserve internal hyphens
    # infixes = list(nlp.Defaults.infixes) + [r'(?<=[0-9a-zA-Z])-(?=[0-9a-zA-Z])']
    # infix_re = compile_infix_regex(infixes)
    # nlp.tokenizer = Tokenizer(nlp.vocab,
    #     prefix_search=nlp.tokenizer.prefix_search,
    #     suffix_search=nlp.tokenizer.suffix_search,
    #     infix_finditer=infix_re.finditer,
    #     token_match=nlp.tokenizer.token_match)
    # STEP 3: ANALYSE DATA
    # Dictionary to store words and counts
    words = {}
    # Rewrite compound words
    for word, comp in COMPWORDS.items():
        pattern = r"\b" + re.escape(word) + r"\b"
        data = re.sub(pattern, comp, data, flags=re.IGNORECASE)
    # Lemmatisation and stopword filtering
    doc = nlp(data)
    for token in doc:
        lemma = token.lemma_.strip()
        if len(lemma) > 3 and lemma not in STOPWORDS:
            if lemma in LEMMAWORDS.keys():
                lemma = LEMMAWORDS[lemma]
            words[lemma] = words.get(lemma, 0) + 1
    # STEP 4: SAVE WORDS
    # Save words and counts to file
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        for word, count in sorted(words.items(), key=lambda x: x[1], reverse=True):
            word = word.replace("_", " ")
            writer.writerow([word, count])
    print_info(f"Words file saved at: {output_file}")

# ===============================================================
# PLOT_WORDCLOUD
# ===============================================================

def plot_wordcloud(words_file, plot_colourmap="viridis", plot_fontpath=None, plot_maxwords=200, special_words=None,\
    special_colour="green", output_file="wordcloud.png"):
    """
    Description:
    ------------
    Generate wordcloud visualisations from word frequency data.
    It generates two images:

    1. A standard wordcloud plot containing all words with
       a gradient colour.
    2. A recoloured version of the same layout, where special
       words are highlighted with a custom colour.

    The word layout remains identical between both images, allowing for
    easy comparison, while only the colours differ.

    Arguments:
    ----------
    words_file      : Input CSV file with words and counts (required).
    plot_colourmap  : Matplotlib colourmap for gradient colouring (optional, default: 'viridis').
    plot_fontpath   : Path to TTF font file (optional, default: None).
    plot_maxwords   : Limit number of words to plot (optional, default: 200).
    special_words   : Comma-separated list of words to highlight in the wordcloud (optional, default: None).
    special_colour  : Colour to highlight special words (optional, default: 'green').
    output_file     : Output PNG file containing the wordcloud (optional, default: 'wordcloud.png').

    Return:
    -------
    None.

    Output:
    -------
    A PNG image of the generated wordcloud is saved to disk. If special words are provided,
    a second image is saved to disk.
    """
    # STEP 1: READ CSV
    # Dictionaty for words and counts
    words = {}
    # Read words
    with open(words_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row["word"]
            count = int(row["count"])
            words[word] = count
    if not words:
        print_warning("No words found to plot")
        return
    # Minimum and maximum counts
    min_freq = min(words.values())
    max_freq = max(words.values())
    # STEP 2: GENERATE WORDCLOUD
    # Get colourmap from Matplotlib
    cmap = plt.get_cmap(plot_colourmap)
    # Custom colour function to colour words according to their size
    def gradient_colour_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Normalise font size
        norm_size = (words[word] - min_freq) / (max_freq - min_freq)
        norm_size = max(0, min(norm_size, 1))
        r, g, b, _ = cmap(norm_size)
        return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"
    # Generate the base wordcloud plot
    wordcloud1 = WordCloud(width=1200, height=600, background_color="white",\
        color_func=gradient_colour_func, max_words=plot_maxwords,\
        font_path=plot_fontpath).generate_from_frequencies(words)
    # Display and save wordcloud plot
    plt.figure(figsize=(15, 7.5))
    plt.imshow(wordcloud1, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_file)
    #plt.show()
    print_info(f"Wordcloud file saved at: {output_file}")
    # Display and save special wordcloud plot
    if special_words:
        # Split special words string
        special_words = [word.strip().lower() for word in special_words.split(",") if word.strip()]
        # Custom colour function for special words
        def special_colour_func(word, font_size, position, orientation, random_state=None, **kwargs):
            if word in special_words:
                return special_colour
            return "lightgray"
        # Recolour wordcloud1 keeping the same layout
        wordcloud2 = wordcloud1.recolor(color_func=special_colour_func)
        # Display and save wordcloud plot
        plt.figure(figsize=(15, 7.5))
        plt.imshow(wordcloud2, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig("special_"+output_file)
        #plt.show()
        print_info(f"Wordcloud file saved at: special_{output_file}")
    plt.close()

# End of file
