import word_processing as wp
import file_handling as fh
import csv
import ast
import regex as re
import os

BATCH_WRITE_SIZE = 1000

TITLE = 0
TEXT = 1
URL = 2
AUTHORS = 3
TAGS = 5

try:
    os.mkdir('indexes') 
except FileExistsError:
    pass

def get_tagged_text(text, section):
    if section == TITLE or section == TEXT:
        return wp.tag_text(text)
    elif section == AUTHORS or section == TAGS:
        return wp.tag_text(' '.join(ast.literal_eval(text)))
    elif section == URL:
        # extracting relevant text from URL using regex
        match = re.search(r"\.[^\/.]+\/(.+)-.+$", text)  # get remaining text after 'medium.com'
        if match:
            # print(f"Extracted text '{' '.join(re.split(r'[/-]', match.group(1)))}' from {text}.")
            return wp.tag_text(' '.join(re.split(r'[/-]', match.group(1))))  # split the text on / or - and join with spaces
        else:
            print(f"Couldn't get URL text from {text}.")
        return wp.tag_text('')


dataset_file = 'practice_dataset2.csv'    # <---------------- change this for indexing a different dataset
lexicon_file = 'indexes/lexicon.csv'
ids_file = 'indexes/next_ids.txt'
forward_index_file = 'indexes/forward_index.csv'
indexed_urls_file = 'indexes/indexed_urls.txt'


next_word_id, next_doc_id = fh.load_ids(ids_file)
lexicon = fh.load_lexicon(lexicon_file)
indexed_urls = fh.load_indexed_urls(indexed_urls_file)
new_urls = set()
indexed = 0

lexicon_entries = []
forward_index_entries = []

try:
    file = open(dataset_file, encoding='utf-8')
    dataset = csv.reader(file)
    next(dataset)    # skip headings row

    for article in dataset:
        # to avoid empty or incomplete rows
        if len(article) < 5:
            continue
        # extract hash from url to check if the article has already been indexed
        this_hash = re.search(r'[^-\/]+$', article[URL]).group()
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
                    lexicon_entries.append([this_word, this_word_id])
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

        forward_index_entries.append([next_doc_id, fh.convert_to_csv(this_entry)])
        next_doc_id += 1

        # write the current batch to the file and clear the entries to save memory
        if indexed % BATCH_WRITE_SIZE == 0:
            print(f"Writing batch {next_doc_id - BATCH_WRITE_SIZE} to {next_doc_id} to forward index file.")
            fh.append_to_csv(forward_index_file, forward_index_entries)
            forward_index_entries = []
    
    # write last entries to forward index
    if forward_index_entries:
        print(f"Writing batch {next_doc_id - (next_doc_id % BATCH_WRITE_SIZE)} to {next_doc_id} to forward index file.")
        fh.append_to_csv(forward_index_file, forward_index_entries)
        forward_index_entries = []
        
finally:
    file.close()

fh.append_to_csv(lexicon_file, lexicon_entries)

# update ids for future indexing
with open(ids_file, 'w') as file:
    file.write(f"{next_word_id}\n{next_doc_id}")

# add new indexed url hashes to file
with open(indexed_urls_file, 'a') as file:
    file.write('\n'.join(new_urls) + '\n')


print(f"\nDone! Indexed {indexed} new documents.")
