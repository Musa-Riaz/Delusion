# this file is currently only for testing
import file_handling as fh
import ast
import struct
import csv
from io import StringIO

# given a word, returns its inverted index entrys
def get_word_docs(word):
    # loads the lexicon, ideally, this will be done only once when the search engine starts
    lexicon = fh.load_lexicon(f'indexes/lexicon.csv')

    # get the word's word id
    try:
        word_id = lexicon[word]
    except KeyError:
        print(f"'{word}' is not a part of the dataset.")
        return []
    
    # calculate the barrel number and position of the word's entry
    barrel = word_id // 1000
    position = word_id % 1000

    # get the offset of this word into the barrel - O(1) operation
    with open(f'indexes/inverted_index/{barrel}.bin', 'rb') as file:
        # offsets are stored as consant sized 4 bit integers
        file.seek(position * 4)
        # position in barrel
        data = file.read(8)
        position = struct.unpack('I', data[0:4])[0]
        next_position = struct.unpack('I', data[4:8])[0]
    
    # seek to the offset position and get the entry - also O(1)
    with open(f'indexes/inverted_index/{barrel}.csv', 'rb') as file:
        file.seek(position)
        data = file.read(next_position - position).decode()
        return ast.literal_eval(ast.literal_eval(data)[1])
    
# returns a document's info (except text) given doc id
def get_doc_info(doc_id):
    with open('indexes/processed.bin', 'rb') as file:
        file.seek(doc_id * 4)
        data = file.read(8)
        pos = struct.unpack('I', data[0:4])[0]
        next_pos = struct.unpack('I', data[4:8])[0]
    
    with open('indexes/processed.csv', 'rb') as file:
        file.seek(pos)
        data = file.read(next_pos - pos).decode()
        # the csv row is obtained as a string
        # read it using a csv reader to get it in a usable format
        string_file = StringIO(data)
        reader = csv.reader(string_file)
        data = next(reader)
        data[3] = ast.literal_eval(data[3])
        data[4] = ast.literal_eval(data[4])
        return data

# word_docs = get_word_docs('apple')
# for i in range(1):
#     print(word_docs[i][1])
#     print(get_doc_info(word_docs[i][0]))
