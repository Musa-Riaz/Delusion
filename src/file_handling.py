import csv
import json
import struct

def load_ids(ids_file):
    try:
        with open(ids_file, 'r') as file:
            return int(file.readline()), int(file.readline())
    except:
        return 0, 0

def load_indexed_urls(indexed_urls_file):
    try:
        with open(indexed_urls_file, 'r', newline='') as file:
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
        print(f"Couldn't open {lexicon_file}.")
        return {}

def load_forward_barrel(forward_barrel_file):
    forward_index = {}
    try:
        with open(forward_barrel_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    this_doc_words = {}
                    for word_id, hit_list in json.loads(row[1].replace("'", '"')):     # replace ' with " for json.loads()
                        this_doc_words[word_id] = hit_list
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
        converted.append([int(id), this_id_hits])
    return converted
    
def write_to_csv(file_name, entries, mode):
    with open(file_name, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(entries)

# creates offsets for a the first byte of each line of a csv file
def create_document_offsets(documents_file):
    # reading 1 mb at a time
    CHUNK_SIZE = 1024 * 1024

    with open(documents_file, 'rb') as file:
        offsets = []
        offset = 0

        while chunk := file.read(CHUNK_SIZE):
            lines = chunk.split(b'\n')
            # skip last line
            for line in lines[:-1]:
                offsets.append(offset)
                offset += len(line) + 1

        offset += len(lines[-1])
    
    return offsets
