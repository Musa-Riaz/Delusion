from sorter import add_to_inv_barrel
import word_processing as wp
import file_handling as fh
import file_paths as fp
import scraper as sp
import regex as re
import struct
import csv
import ast
import os

# write the data to forward index in batches of..
BATCH_WRITE_SIZE = 1000

# in words
BARREL_SIZE = 1000

TITLE = 0
TEXT = 1
URL = 2
AUTHORS = 3
TIMESTAMP = 4
TAGS = 5

def get_tagged_text(text, section):
    if section == TITLE or section == TEXT:
        return wp.tag_text(text)
    elif section == AUTHORS or section == TAGS:
        return wp.tag_text(' '.join(ast.literal_eval(text)))
    elif section == URL:
        # extracting relevant text from URL using regex
        match = re.search(r"\.[^\/.]+\/(.+)-.+$", text)  # get remaining text after 'medium.com'
        if match:
            return wp.tag_text(' '.join(re.split(r'[/-]', match.group(1))))  # split the text on / or - and join with spaces
        else:
            print(f"Couldn't get URL text from {text}.")
        return wp.tag_text('')

def index_article(article, indexed_urls, lexicon, lexicon_entries, forward_index_entries, new_urls, processed_docs):
    global next_word_id, next_doc_id
    # to avoid empty or incomplete rows
    if len(article) < 5:
        return
    # extract hash from url to check if the article has already been indexed
    this_hash = re.search(r'[^-\/]+$', article[URL]).group()
    if this_hash in indexed_urls or this_hash in new_urls:
        print(f"{this_hash} already indexed.")
        return

    new_urls.add(this_hash)
    print(f"Indexing {this_hash}...")
    processed_docs.append([next_doc_id, article[TITLE], article[URL], article[AUTHORS], article[TAGS], article[TIMESTAMP]])
    
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
    
    # write the text to the texts file, this is done here as keeping multiple entire texts in memory is not feasible
    fh.append_offset(fp.texts_file)
    fh.write_to_csv(fp.texts_file + '.csv', [[next_doc_id, article[TEXT]]], 'a')
    
    next_doc_id += 1
    

# writes forward entries, additionally updates inverted index based on a provided flag
def write_forward_entries(forward_index_entries, processed_docs, forward_index_folder, processed_docs_file, update_inverted=False):
    fh.write_to_csv(processed_docs_file + '.csv', processed_docs, 'a')
    for i in range(len(forward_index_entries)):
        if forward_index_entries[i]:
            # writes to the specific barrels
            # barrels are name as n.csv where n is the barrel number
            fh.write_to_csv(forward_index_folder + f'/{i}.csv', forward_index_entries[i], 'a')
            if update_inverted:
                add_to_inv_barrel(forward_index_entries[i][0], i)
                
            
# indexes a csv dataset, provided as a file path
# if the is_new_doc flag is set to True, the function assumes one document will be provided to be added to an existing index
# and updates the inverted index entries as required too
def index_csv_dataset(dataset, lexicon, ids_file, forward_index_folder, indexed_urls_file, processed_docs_file, is_new_doc=True, scrape=False):
    os.makedirs('indexes/forward_index', exist_ok=True)

    global next_word_id, next_doc_id
    next_word_id, next_doc_id = fh.load_ids(ids_file)
    if scrape:
        scraped_data = sp.scrape_medium_article(dataset['url'])
        try:
            scraped_data['thumbnail_url']
        except KeyError:
            return scraped_data     # error while scraping
    elif is_new_doc:
        scraped_data = dataset
    
    if is_new_doc: 
        fh.append_offset(fp.scraped_file)
        fh.write_to_csv(fp.scraped_file + '.csv', [[next_doc_id, scraped_data['thumbnail_url'], scraped_data['members_only']]], 'a')
        dataset = [json_to_csv(dataset)]
        
    if not is_new_doc:
        lexicon = fh.load_lexicon(lexicon)
    indexed_urls = fh.load_indexed_urls(indexed_urls_file)
    new_urls = set()

    lexicon_entries = []
    forward_index_entries = []
    processed_docs = []

    try:
        file = None
        if not is_new_doc:
            file = open(dataset, encoding='utf-8')
            dataset = csv.reader(file)
            next(dataset)    # skip headings row
        
        for article in dataset:
            index_article(article, indexed_urls, lexicon, lexicon_entries, forward_index_entries, new_urls, processed_docs)
            
            # write the current batch to the files and clear the entries to save memory
            if next_doc_id % BATCH_WRITE_SIZE == 0:
                print(f"Writing batch {next_doc_id - BATCH_WRITE_SIZE} to {next_doc_id} to forward index file.")
                write_forward_entries(forward_index_entries, processed_docs, forward_index_folder, processed_docs_file)
                processed_docs = []
                forward_index_entries = []

        # write last entries to forward index barrels
        write_forward_entries(forward_index_entries, processed_docs, forward_index_folder, processed_docs_file, is_new_doc)
        # update the inverted index entries too, if a document is beign added
            
    except IOError:
        print(f"Couldn't open {dataset}")
    finally:
        if file:
            file.close()

    fh.write_to_csv(fp.lexicon_file, lexicon_entries, 'a')

    # create and write offsets for processed documents
    offsets = fh.create_document_offsets(processed_docs_file + '.csv')
    with open(processed_docs_file + '.bin', 'wb') as file:
        file.write(b''.join(struct.pack('I', offset) for offset in offsets))

    # update ids for future indexing
    with open(ids_file, 'w') as file:
        file.write(f"{next_word_id}\n{next_doc_id}")

    # add new indexed url hashes to file
    with open(indexed_urls_file, 'a') as file:
        file.write('\n'.join(new_urls) + '\n')

    print(f"\nDone! Indexed up to doc_id {next_doc_id}.")


def json_to_csv(json):
    return [json['title'], json['text'], json['url'], json['authors'], json['timestamp'], json['tags']]

# index_csv_dataset(dataset_file, lexicon_file, ids_file, forward_index_folder, indexed_urls_file, processed_docs_file)
