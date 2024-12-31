import word_processing as wp
import file_handling as fh
import file_paths as fp
import threading as th
import ranking as rk
import struct
import json
import ast
import re

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

    data = fh.read_with_offset(position, fp.inverted_index_folder + f'/{barrel}')
    data = json.loads(data[1])
    results[word] = data

    
# returns a document's info (except text) given doc id
def get_doc_info(doc_id, results, query, scraped):
    processed_info, text = [], []
    processed_thread = th.Thread(target=get_processed_data, args=(doc_id, processed_info))
    desc_thread = th.Thread(target=get_description, args=(doc_id, text, query))
    
    processed_thread.start()
    desc_thread.start()
    processed_thread.join()
    desc_thread.join()
    
    # [doc_id, title, url, authors, tags, timestamp, img_url, members_only, description] is being returned
    results.append(convert_to_json(processed_info[0] + scraped[doc_id][1:] + text))
    
# for threading in get_doc_info()
def get_processed_data(doc_id, processed_info):
    data = fh.read_with_offset(doc_id, fp.processed_docs_file)
    data[3] = ast.literal_eval(data[3])
    data[4] = ast.literal_eval(data[4])
    processed_info.append(data)

def get_description(doc_id, text, query):
    data = fh.read_with_offset(doc_id, fp.texts_file)
    text.append(find_relevant_desc(data[1], query, 130))
    
# returns ~n characters starting from the sentence containing the provided word in the given text
# returns the first ~n characters if word doesnt exist
def find_relevant_desc(text, query, n):
    word = query[0]
    # split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    index = 0
    # find sentence containing word
    for i in range(len(sentences)):
        if re.search(rf'\b{re.escape(word)}\b', sentences[i], re.IGNORECASE):
            index = i

    result = ''
    for sentence in sentences[index:]:
        for word in sentence.split():
            if word.lower() in query:
                result += '<b>' + word + r'<\b>'    # highlight this word
            else:
                result += word
            result += ' '
            if len(result) > n:
                return result + "..."
    return result + "..."

def convert_to_json(doc):
    doc_dict = {}
    doc_dict['title'] = doc[1]
    doc_dict['url'] = doc[2]
    doc_dict['description'] = doc[8]
    doc_dict['imageUrl'] = doc[6] if doc[6] != "No thumbnail available" else ''
    doc_dict['tags'] = doc[4]
    doc_dict['timeStamps'] = [doc[5][:10]]
    doc_dict['authors'] = ', '.join(doc[3])
    return doc_dict

def get_results(query, lexicon, scraped, start, end, members_only):
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
                # article is deleted, skip
                if scraped[doc[1]][2] == 'Unknown':
                    continue
                
                # request to not show members-only articles, skip members-only articles
                if not members_only and scraped[doc[1]][2] == 'Yes':
                    continue
                
                if doc[1] not in result_docs_set:
                    result_docs.append(doc)
                result_docs_set.add(doc[1])
    
    result_docs = list(result_docs)
    results = []
    threads = []
    for i in range(start, end):
        if i >= len(result_docs):
            break
        this_thread = th.Thread(target=get_doc_info, args=(result_docs[i][1], results, query, scraped))
        threads.append(this_thread)
        this_thread.start()
        
    for thread in threads:
        thread.join()

    return results, len(result_docs)
