from io import StringIO
import struct
import json
import csv
import ast

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

def load_scraped(scraped_file):
    with open(scraped_file, 'r', newline='', encoding='utf-8') as file:
        scraped = file.readlines()
        for i in range(len(scraped)):
            scraped[i] = scraped[i].strip().split(',')
    return scraped

# loads constant-sized data stored in binary into a list
def load_binary_data(file, struct_size = 4):
    try:
        with open(file, 'rb') as file:
            data = file.read()
            num_structs = len(data) // struct_size
            structs = struct.unpack(f'{num_structs}i', data)
            return structs
    except IOError:
        print(f"Couldn't open {file}.")
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
    offsets = []
    
    with open(documents_file, 'rb') as file:
        current_offset = 0
        
        reader = csv.reader((line.decode('utf-8') for line in file), quotechar='"', delimiter=',')
        
        for row in reader:
            offsets.append(current_offset)
            current_offset = file.tell()
    
    return offsets

# appends a new offset to the end of a binary offset file
# the new offset is simply the end of the file, as this is the start of the 'next' line
# should be called BEFORE adding a new entry
def append_offset(file_path):
    with open(file_path + '.csv', 'rb') as file:
        file.seek(0, 2)
        new_offset = file.tell()
    
    with open(file_path + '.bin', 'ab') as file:
        file.write(struct.pack('I', new_offset))

# reads a row based on offsets
def read_with_offset(row_num, file_name):
    csv.field_size_limit(10000000)
    with open(file_name + '.bin', 'rb') as file:
        file.seek(row_num * 4)
        data = file.read(8)
        pos = struct.unpack('I', data[0:4])[0]
        try:
            next_pos = struct.unpack('I', data[4:8])[0]
        except:
            next_pos = 0        # in case of last row
    
    with open(file_name + '.csv', 'rb') as file:
        file.seek(pos)
        if next_pos != 0:
            data = file.read(next_pos - pos).decode()
        else:
            data = file.read().decode()     # last row - read all remaining data
        # the csv row is obtained as a string
        # read it using a csv reader to get it in a usable format
        string_file = StringIO(data)
        reader = csv.reader(string_file)
        data = next(reader)
        return data
