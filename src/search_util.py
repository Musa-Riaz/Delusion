# this file is currently only for testing
import file_handling as fh
import ast
import struct
import csv
from io import StringIO
from sortedcontainers import SortedList
import word_processing as wp
import threading as th

# given a word, returns its inverted index entrys
def get_word_docs(word, lexicon, results):
    # get the word's word id
    try:
        word_id = lexicon[word]
    except KeyError:
        print(f"'{word}' is not a part of the dataset.")
        results[word] = []
    
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
        results[word] = ast.literal_eval(ast.literal_eval(data)[1])
    
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
    
TITLE = 0
TEXT = 1
URL = 2
AUTHORS = 3
TAGS = 5

def min_index(array):
    min = array[0][1]
    for i in range(1, len(array)):
        if array[i][1] < array[min][1]:
            min = i
    return min

def rank_docs(docs, n):
    top_docs = SortedList()
    lowest_top_score = 0
    for doc in docs:
        this_score = min(len(doc[1]), 100)
        for hit in doc[1]:
            if hit % 10 == TITLE:
                this_score += 50
            elif hit % 10 == URL:
                this_score += 30
            elif hit % 10 == AUTHORS:
                this_score += 40
            elif hit % 10 == TAGS:
                this_score += 30

            if hit % 10 != TEXT:
                break
        
        # storing negative score for 'descending' order
        if len(top_docs) < n:
            top_docs.add((-1 * this_score, doc[0]))
        elif this_score > lowest_top_score:
            # pop removes 'minimum' score
            top_docs.pop()
            top_docs.add((-1 * this_score, doc[0]))
            lowest_top_score = top_docs[-1][0]
        
        if len(top_docs) == n and lowest_top_score < -80:
            break
    
    print([doc[0] for doc in top_docs])
    return [doc[1] for doc in top_docs]

def convert_to_json(doc):
    doc_dict = {}
    doc_dict['title'] = doc[1]
    doc_dict['url'] = doc[2]
    doc_dict['description'] = 'THIS IS DESCRIPTION HEHE'
    doc_dict['imageUrl'] = 'https://buzz-plus.com/wp-content/uploads/2021/04/cutest-monkey-video-in-the-world.jpg'
    doc_dict['tags'] = doc[4]
    doc_dict['timeStamps'] = ['now', 'then']
    return doc_dict

def get_results(query, n, lexicon):
    query = wp.process_query(query)
    print(query)

    words = {}
    threads = []
    for word in query:
        this_thread = th.Thread(target=get_word_docs, args=(word, lexicon, words))
        threads.append(this_thread)
        this_thread.start()
    
    for thread in threads:
        thread.join()

    docs = get_word_docs(query.pop(), lexicon)
    results = []
    if docs:
        docs = rank_docs(docs, n)
        for i in range(len(docs)):
            this_doc = get_doc_info(docs[i])
            results.append(convert_to_json(this_doc))
    return results
