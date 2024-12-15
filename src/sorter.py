# this is the sorter of the search engine, converting forward index into inverted index
# initial version, assumes no barrels are implemented, not intended to function efficiently for the entire forward index without barrel divisions
import file_handling as fh

forward_index_file = 'indexes/forward_index.csv'
inverted_index_file = 'indexes/inverted_index.csv'

forward_index = fh.load_forward_index(forward_index_file)
inverted_index = {}
sorted_counter = 0

print("Sorting...")
for doc_id in forward_index:
    sorted_counter += 1
    # this_index is all the words in the current document with their hitlists
    this_index = forward_index[doc_id]
    for word_id in this_index:
        if word_id not in inverted_index:
            # initialize a dict for this word_id
            inverted_index[word_id] = {}
        # append this {doc_id : hitlist} to this word's entry
        inverted_index[word_id][doc_id] = this_index[word_id]

inverted_index_entries = []
# looping through a copy of the word_id keys
# each entry is converted to a writeable csv and then deleted from the dictionary
# this uses additional memory for the copy of the keys, however, as the values
# are much larger than the keys, it saves a significant amount of memory
for word_id in list(inverted_index.keys()):
    inverted_index_entries.append([word_id, fh.convert_to_csv(inverted_index[word_id])])
    del inverted_index[word_id]

fh.append_to_csv(inverted_index_file, inverted_index_entries)
print(f"Sorted {sorted_counter} documents.")
