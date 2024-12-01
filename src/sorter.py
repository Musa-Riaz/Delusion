# this is the sorter of the search engine, converting forward index into inverted index
# initial version, assumes no barrels are implemented, not intended to function efficiently for the entire forward index without barrel divisions
import json

forward_index_file = 'indexes/forward_index.json'
inverted_index_file = 'indexes/inverted_index.json'

with open(forward_index_file, 'r') as file:
    forward = json.load(file)

inverted = {}
sorted = 0

for doc_id in forward:
    sorted += 1
    # this_index is all the words in the current document with their hitlists
    this_index = forward[doc_id]
    for word_id in this_index:
        if word_id not in inverted:
            # initialize a dict for this word_id
            inverted[word_id] = {}
        # append this {doc_id : hitlist} to this word's entry
        inverted[word_id][doc_id] = this_index[word_id]

with open(inverted_index_file, 'w') as file:
    json.dump(inverted, file)

print(f"Sorted {sorted} documents.")