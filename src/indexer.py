import word_processing as wp
import file_handling as fh
import csv
import ast
import regex as re
import os

# write the data to forward index in batches of..
BATCH_WRITE_SIZE = 1000

# in words
BARREL_SIZE = 1000

TITLE = 0
TEXT = 1
URL = 2
AUTHORS = 3
TAGS = 5

os.makedirs('indexes/forward_index', exist_ok=True)

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


dataset_file = 'n_articles.csv'    # <---------------- change this for indexing a different dataset
lexicon_file = 'indexes/lexicon.csv'
ids_file = 'indexes/next_ids.txt'
forward_index_folder = 'indexes/forward_index'
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

        # these entries will contain an entry for this document in each barrel
        # these_entries[0] is this document's entry in barrel 0, 1 in 1 and so on...
        these_entries = []
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
                
                # add barrels if necessary
                barrel = this_word_id // BARREL_SIZE
                # if these_entries doesn't have the respective barrel, add it
                if len(these_entries) < barrel + 1:
                    these_entries.extend([{} for i in range(barrel - len(these_entries) + 1)])
                
                # initialize new hitlist if first occurence
                if this_word_id not in these_entries[barrel]:
                    these_entries[barrel][this_word_id] = []

                # pos * 10 + section is hit representation
                # first 4 digits show position, last digit shows section
                these_entries[barrel][this_word_id].append(pos * 10 + section)

                # cap position at 9999
                if pos < 9999:
                    pos += 1

        # appending this document to the forward index entries
        # forward index entries contains entries for multiple documents in each barrel
        for barrel in range(len(these_entries)):
            if len(forward_index_entries) < barrel + 1:
                    forward_index_entries.extend([[] for i in range(barrel - len(forward_index_entries) + 1)])
            forward_index_entries[barrel].append([next_doc_id, fh.convert_to_csv(these_entries[barrel])])
        
        next_doc_id += 1

        # write the current batch to the files and clear the entries to save memory
        if indexed % BATCH_WRITE_SIZE == 0:
            print(f"Writing batch {next_doc_id - BATCH_WRITE_SIZE} to {next_doc_id} to forward index file.")
            for i in range(len(forward_index_entries)):
                if forward_index_entries[i]:
                    # writes to the specific barrels
                    # barrels are name as n.csv where n is the barrel number
                    fh.write_to_csv(forward_index_folder + f'/{i}.csv', forward_index_entries[i], 'a')
            forward_index_entries = []
    
    # write last entries to forward index barrels
    if forward_index_entries:
        print(f"Writing batch {next_doc_id - (next_doc_id % BATCH_WRITE_SIZE)} to {next_doc_id} to forward index file.")
        for i in range(len(forward_index_entries)):
                if forward_index_entries[i]:
                    fh.write_to_csv(forward_index_folder + f'/{i}.csv', forward_index_entries[i], 'a')
        forward_index_entries = []
        
finally:
    file.close()

fh.write_to_csv(lexicon_file, lexicon_entries, 'a')

# update ids for future indexing
with open(ids_file, 'w') as file:
    file.write(f"{next_word_id}\n{next_doc_id}")

# add new indexed url hashes to file
with open(indexed_urls_file, 'a') as file:
    file.write('\n'.join(new_urls) + '\n')


print(f"\nDone! Indexed {indexed} new documents.")
