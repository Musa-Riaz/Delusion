# this file is currently only for testing
import file_handling as fh
import json
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

def rank_docs(docs, n, intersections):
    # TITLE = 0
    # TEXT = 1
    # URL = 2
    # AUTHORS = 3
    # TAGS = 5
    added = [False for i in range(6)]
    top_docs = SortedList()
    for doc in docs:
        this_score = min(len(doc[1]), 50)
        multiplier = 1
        for i in range(len(intersections) - 1, -1, -1):
            if doc[0] in intersections[i]:
                multiplier = (i + 1) * 2
                this_score += 30
                # TODO : implement proximity ranking
                break

        i = 0
        step = 1
        while i < len(doc[1]) and i >= 0:
            hit = doc[1][i]
            match hit % 10: 
                case 0:
                    if not added[0]:
                        this_score += 50
                        added[0] = True
                case 2:
                    if not added[2]:
                        this_score += 30
                        added[2] = True
                case 3:
                    if not added[3]:
                        this_score += 40
                        added[3] = True
                case 5:
                    if not added[5]:
                        this_score += 30
                        added[5] = True
            
            # hits are stored in order, with TEXT hits in between TITLE and AUTHOR hits
            # if a TEXT hit is encounted, all relevant hits are behind <i>
            # so jump to the end of the list to process TAGS and AUTHORS hits
            if hit % 10 == 1:
                if step == 1:
                    i = len(doc[1]) - 1
                    step = -1
                else:
                    # the pointer is going backwards and reached a TEXT hit, meaning all relevant hits have been processed
                    break
            else:
                i += step

        this_score *= multiplier
        # storing negative score for 'descending' order
        #if len(top_docs) < n:
        top_docs.add((-1 * this_score, doc[0]))
        # elif this_score > lowest_top_score:
        #     # pop removes 'minimum' score
        #     top_docs.pop()
        #     top_docs.add((-1 * this_score, doc[0]))
        #     lowest_top_score = top_docs[-1][0]
        
        # if len(top_docs) == n and lowest_top_score < -80:
        #     break
    
    return top_docs

def convert_to_json(doc):
    doc_dict = {}
    doc_dict['title'] = doc[1]
    doc_dict['url'] = doc[2]
    doc_dict['description'] = 'THIS IS DESCRIPTION HEHE'
    doc_dict['imageUrl'] = 'https://buzz-plus.com/wp-content/uploads/2021/04/cutest-monkey-video-in-the-world.jpg'
    doc_dict['tags'] = doc[4]
    doc_dict['timeStamps'] = ['now']
    return doc_dict

def get_results(query, n, lexicon):
    query = wp.process_query(query)

    words = {}
    threads = []
    for word in query:
        this_thread = th.Thread(target=get_word_docs, args=(word, lexicon, words))
        threads.append(this_thread)
        this_thread.start()
    
    for thread in threads:
        thread.join()

    intersections = []
    if len(words) > 1:
        doc_ids = [[doc_hits[0] for doc_hits in docs] for docs in words.values()]

        intersections.append(set(doc_ids[0]).intersection(doc_ids[1]))
        for i in range(2, len(doc_ids)):
            intersections.append(intersections[i-2].intersection(doc_ids[i]))

    print(intersections)    
    result_docs_set = set()
    result_docs = []
    for docs in words.values():
        if docs:
            for doc in rank_docs(docs, 1, intersections):
                if doc[1] not in result_docs_set:
                    result_docs.append(doc[1])
                result_docs_set.add(doc[1])
    
    result_docs = list(result_docs)
    NUM_RESULTS = 8
    results = []
    for i in range(min(len(result_docs), NUM_RESULTS)):
        results.append(convert_to_json(get_doc_info(result_docs[i])))

    return results
