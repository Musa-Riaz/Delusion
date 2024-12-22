from ranking import rank_docs
from io import StringIO
import word_processing as wp
import threading as th
import struct
import json
import ast
import csv

# given a word, returns its inverted index entries
def get_word_docs(word, lexicon, results):
    # get the word's word id
    try:
        word_id = lexicon[word]
    except KeyError:
        print(f"'{word}' is not a part of the dataset.")
        results[word] = []
        return
    
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
        data = json.loads(ast.literal_eval(data)[1])
        results[word] = data

    
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

def convert_to_json(doc, score):
    doc_dict = {}
    doc[4].extend([score, doc[0]])
    doc_dict['title'] = doc[1]
    doc_dict['url'] = doc[2]
    doc_dict['description'] = 'THIS IS DESCRIPTION HEHE'
    doc_dict['imageUrl'] = r'https://www.meme-arsenal.com/memes/5d2155364664354f74ceec5ecd9e6e8c.jpg'
    doc_dict['tags'] = doc[4]
    doc_dict['timeStamps'] = ['now']
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

    intersections = intersect(words.values())

    result_docs_set = set()
    result_docs = []
    for docs in words.values():
        if docs:
            for doc in rank_docs(docs, intersections):
                if doc[1] not in result_docs_set:
                    result_docs.append(doc)
                result_docs_set.add(doc[1])
    
    result_docs = list(result_docs)
    results = []
    for i in range(min(len(result_docs), n)):
        results.append(convert_to_json(get_doc_info(result_docs[i][1]), result_docs[i][0]))

    return results

def intersect(doc_lists):
    if len(doc_lists) <= 1:
        return []
    
    doc_lists = [{doc[0] : is_relevant(doc[1]) for doc in doc_list} for doc_list in doc_lists]
    intersections = [doc_lists[0]]
    
    for i in range(1, len(doc_lists)):
        this_intersection = {}
        for doc_id in doc_lists[i]:
            if doc_id in intersections[i - 1]:
                if doc_lists[i][doc_id] and intersections[i - 1][doc_id]:
                    this_intersection[doc_id] = True
                else:
                    this_intersection[doc_id] = False
        intersections.append(this_intersection)
    return intersections
        
# a hit list is considered relevant if it contains any hits other than text
def is_relevant(hit_list):
    # hit lists store hits in order title, text, url, author, tags
    # so only the first and last hits can be relevant
    return hit_list[0] % 10 != 1 or hit_list[-1] % 10 != 1