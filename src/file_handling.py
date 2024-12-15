import csv
import json

def load_ids(ids_file):
    try:
        with open(ids_file, 'r') as file:
            return int(file.readline()), int(file.readline())
    except:
        return 0, 0

def load_indexed_urls(indexed_urls_file):
    try:
        with open(indexed_urls_file, 'r') as file:
            return set(file.read().splitlines())
    except IOError:
        return set()
    
def load_lexicon(lexicon_file):
    lexicon = {}
    try:
        with open(lexicon_file) as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    lexicon[row[0]] = int(row[1])
            return lexicon
    except IOError:
        print(f"Couldn't open {lexicon_file}, starting with empty lexicon...")
        return {}

def load_forward_index(forward_index_file):
    forward_index = {}
    try:
        with open(forward_index_file) as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    this_doc_words = {}
                    for word, hit_list in json.loads(row[1].replace("'", '"')):     # replace ' with " for json.loads()
                        this_doc_words[word] = hit_list
                    forward_index[row[0]] = this_doc_words
            return forward_index
    except IOError:
        print(f"Couldn't open {forward_index}, starting with empty forward index...")
        return {}
    
def convert_to_csv(index_entry):
    converted = []
    for id in index_entry:
        this_id_hits = []
        for hit in index_entry[id]:
            this_id_hits.append(hit)
        converted.append([id, this_id_hits])
    return converted
    
def append_to_csv(file_name, entries):
    with open(file_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(entries)
