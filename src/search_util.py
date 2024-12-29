import word_processing as wp
import file_handling as fh
import threading as th
import ranking as rk
import struct
import json
import ast

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
def get_doc_info(doc_id, results):
    processed_info, scraped_info = [], []
    processed_thread = th.Thread(target=get_processed_data, args=(doc_id, processed_info))
    scraped_thread = th.Thread(target=get_scraped_data, args=(doc_id, scraped_info))
    
    processed_thread.start()
    scraped_thread.start()
    processed_thread.join()
    scraped_thread.join()
    
    # [doc_id, title, url, authors, tags, timestamp, img_url, members_only] is being returned
    results.append(convert_to_json(processed_info[0] + scraped_info[0][1:]))
    
# for threading in get_doc_info()
def get_processed_data(doc_id, processed_info):
    data = fh.read_with_offset(doc_id, 'indexes/processed')
    data[3] = ast.literal_eval(data[3])
    data[4] = ast.literal_eval(data[4])
    processed_info.append(data)

def get_scraped_data(doc_id, scraped_info):
    try:
        data = fh.read_with_offset(doc_id, 'indexes/scraped')
    except:
        scraped_info.append(['', ''])
    scraped_info.append(data)

def convert_to_json(doc):
    doc_dict = {}
    doc_dict['title'] = doc[1]
    doc_dict['url'] = doc[2]
    doc_dict['description'] = 'THIS IS DESCRIPTION HEHE'
    doc_dict['imageUrl'] = doc[6]
    doc_dict['tags'] = doc[4]
    doc_dict['timeStamps'] = [doc[5][:10]]
    doc_dict['authors'] = ', '.join(doc[3])
    return doc_dict

def get_results(query, lexicon, start, end):
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

    intersections = rk.intersect(words.values())

    result_docs_set = set()
    result_docs = []
    for docs in words.values():
        if docs:
            for doc in rk.rank_docs(docs, intersections):
                if doc[1] not in result_docs_set:
                    result_docs.append(doc)
                result_docs_set.add(doc[1])
    
    result_docs = list(result_docs)
    results = []
    threads = []
    for i in range(start, end):
        if i >= len(result_docs):
            break
        this_thread = th.Thread(target=get_doc_info, args=(result_docs[i][1], results))
        threads.append(this_thread)
        this_thread.start()
        
    for thread in threads:
        thread.join()

    return results, len(result_docs)
