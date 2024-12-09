import word_processing as wp
import csv
import json
import regex as re
import os

TITLE = 0
TEXT = 1
URL = 2
AUTHORS = 3
TAGS = 5

try:
    os.mkdir('indexes')
except FileExistsError:
    pass

def load_ids(ids_file):
    try:
        with open(ids_file, 'r') as file:
            return int(file.readline()), int(file.readline())
    except:
        return 0, 0

def load_lexicon(lexicon_file):
    try:
        with open(lexicon_file) as file:
            return json.load(file)
    except IOError:
        return {}

def load_indexed_urls(indexed_urls_file):
    try:
        with open(indexed_urls_file, 'r') as file:
            return set(file.read().splitlines())
    except IOError:
        return set()
    
def load_forward_index(forward_index_file):
    try:
        with open(forward_index_file) as file:
            return json.load(file)
    except IOError:
        return {}

def get_tagged_text(text, section):
    if section == TITLE or section == TEXT:
        return wp.tag_text(text)
    elif section == AUTHORS or section == TAGS:
        return wp.tag_text(' '.join(eval(text)))
    elif section == URL:
        # extracting relevant text from URL using regex
        match = re.search(r"medium\.com\/(.+)-(.+)$", text)  # get remaining text after 'medium.com'
        if match:
            return wp.tag_text(' '.join(re.split(r'[/-]', match.group(1))))  # split the text on / or - and join with spaces
        return wp.tag_text('')


dataset_file = '10_articles.csv'    # <---------------- change this for indexing a different dataset
lexicon_file = 'indexes/lexicon.json'
ids_file = 'indexes/next_word_id.txt'
forward_index_file = 'indexes/forward_index.json'
indexed_urls_file = 'indexes/indexed_urls.txt'


next_word_id, next_doc_id = load_ids(ids_file)
lexicon = load_lexicon(lexicon_file)
indexed_urls = load_indexed_urls(indexed_urls_file)
new_urls = set()
forward_index = load_forward_index(forward_index_file)
indexed = 0

try:
    file = open(dataset_file, encoding='utf-8')
    dataset = csv.reader(file)
    next(dataset)    # skip headings row

    for article in dataset:
        # to avoid empty or incomplete rows
        if len(article) < 5:
            continue
        # extract hash from url to check if the article has already been indexed
        this_hash = re.search(r'[^-]+$', article[URL]).group()
        if this_hash in indexed_urls or this_hash in new_urls:
            print(f"{this_hash} already indexed.")
            continue

        new_urls.add(this_hash)
        print(f"Indexing {this_hash}...")
        indexed += 1

        this_entry = {}
        for section in [TITLE, TEXT, URL, AUTHORS, TAGS]:
            pos = 0

            tagged_text = get_tagged_text(article[section], section)

            for word, tag in tagged_text:
                this_word = wp.process_word(word, tag)

                if this_word == '':
                    continue

                # add word to new words, to be appended later to the lexicon file
                if this_word not in lexicon:
                    this_word_id = next_word_id
                    lexicon[this_word] = this_word_id
                    next_word_id += 1
                else:
                    this_word_id = lexicon[this_word]

                # initialize new hitlist if first occurence
                if this_word_id not in this_entry:
                    this_entry[this_word_id] = []

                # pos * 10 + section is hit representation
                # first 4 digits show position, last digit shows section
                this_entry[this_word_id].append(pos * 10 + section)

                # cap position at 9999
                if pos < 9999:
                    pos += 1

        forward_index[next_doc_id] = this_entry
        next_doc_id += 1
        
finally:
    file.close()

with open(lexicon_file, 'w') as file:
    json.dump(lexicon, file)

with open(forward_index_file, 'w') as file:
    json.dump(forward_index, file)

# update ids for future indexing
with open(ids_file, 'w') as file:
    file.write(f"{next_word_id}\n{next_doc_id}")

# add new indexed url hashes to file
try:
    file = open(indexed_urls_file, 'a')
    file.write('\n'.join(new_urls) + '\n')
except IOError:
    file = open(indexed_urls_file, 'w')
    file.write('\n'.join(new_urls) + '\n')
finally:
    file.close()

print(f"\nDone! Indexed {indexed} new documents.")
