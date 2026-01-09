import os
import re
import math
import json
from collections import defaultdict
from html import unescape

PAGES_DIR = "saved_pages"
INVERTED_INDEX_FILE = "inverted_index.json"
IDF_FILE = "idf.json"

STOPWORDS = {"the","is","in","and","to","of","a","on","for","with","as","by","an","be","are","this","that","from","or","at"}

def parse_html(html):
    html = re.sub(r"<script.*?>.*?</script>", " ", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?>.*?</style>", " ", html, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", html)
    return unescape(text)

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return [t for t in text.split() if t not in STOPWORDS and len(t) > 2]

def compute_tf(tokens):
    tf = defaultdict(int)
    for t in tokens:
        tf[t] += 1
    total = len(tokens)
    for t in tf:
        tf[t] /= total
    return tf

def build_index():
    inverted_index = defaultdict(dict)
    doc_freq = defaultdict(int)
    total_docs = 0

    for file in os.listdir(PAGES_DIR):
        if not file.endswith(".html"):
            continue
        total_docs += 1
        with open(os.path.join(PAGES_DIR, file), encoding="utf-8", errors="ignore") as f:
            tokens = tokenize(parse_html(f.read()))
        tf = compute_tf(tokens)
        for term, value in tf.items():
            inverted_index[term][file] = value
        for term in set(tokens):
            doc_freq[term] += 1

    return inverted_index, doc_freq, total_docs

def compute_idf(df, total_docs):
    return {term: math.log(total_docs / freq) for term, freq in df.items()}

def save_files(index, idf):
    with open(INVERTED_INDEX_FILE, "w") as f:
        json.dump(index, f, indent=4)
    with open(IDF_FILE, "w") as f:
        json.dump(idf, f, indent=4)

if __name__ == "__main__":
    index, df, total_docs = build_index()
    idf = compute_idf(df, total_docs)
    save_files(index, idf)
