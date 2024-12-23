from io import StringIO
import struct
import json
import csv

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

def load_frequencies(frequencies_file):
    try:
        with open(frequencies_file, 'rb') as file:
            data = file.read()
            num_freq = len(data) // 4
            frequencies = struct.unpack(f'{num_freq}i', data)
            return frequencies
    except IOError:
        print(f"Couldn't open {frequencies_file}.")
        return []
    
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
    with open(documents_file, 'rb') as file:
        offsets = []
        offset = 0

        for line in file:
            offsets.append(offset)
            offset += len(line)
    
    return offsets

def create_document_offsets(documents_file):
    offsets = []
    
    with open(documents_file, 'rb') as file:
        current_offset = 0
        
        reader = csv.reader((line.decode('utf-8') for line in file), quotechar='"', delimiter=',')
        
        for row in reader:
            offsets.append(current_offset)
            current_offset = file.tell()
    
    return offsets

# reads a row based on offsets
def read_with_offset(row_num, file_name):
    with open(file_name + '.bin', 'rb') as file:
        file.seek(row_num * 4)
        data = file.read(8)
        pos = struct.unpack('I', data[0:4])[0]
        next_pos = struct.unpack('I', data[4:8])[0]
    
    with open(file_name + '.csv', 'rb') as file:
        file.seek(pos)
        data = file.read(next_pos - pos).decode()
        # the csv row is obtained as a string
        # read it using a csv reader to get it in a usable format
        string_file = StringIO(data)
        reader = csv.reader(string_file)
        data = next(reader)
        return data
