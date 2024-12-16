import file_handling as fh
import os
import struct

def get_byte_size(entry):
    entry[1] = '"' + str(entry[1]) + '"'
    csv_line = ','.join(map(str, entry)) + '\n'
    return len(csv_line)

forward_index_folder = 'indexes/forward_index'
inverted_index_folder = 'indexes/inverted_index'

os.makedirs('indexes/inverted_index', exist_ok=True)

barrel_number = 0
sorted_counter = 0
while True:
    barrel_path = forward_index_folder + f'/{barrel_number}.csv'
    if os.path.isfile(barrel_path):
        forward_barrel = fh.load_forward_barrel(barrel_path)
        inverted_barrel = {}
        
        print(f"Sorting barrel {barrel_number}...")
        for doc_id in list(forward_barrel.keys()):
            # this_index is all the words in the current document with their hitlists
            this_index = forward_barrel[doc_id]
            
            # free memory of this forward entry
            del forward_barrel[doc_id]

            for word_id in this_index:
                if word_id not in inverted_barrel:
                    # initialize a dict for this word_id
                    inverted_barrel[word_id] = {}

                # append this {doc_id : hitlist} to this word's entry
                inverted_barrel[word_id][doc_id] = this_index[word_id]
        
        inverted_barrel_entries = []
        offsets = []
        offset = 0
        # looping through a copy of the word_id keys
        # each entry is converted to a writeable csv and then deleted from the dictionary
        # this uses additional memory for the copy of the keys, however, as the values
        # are much larger than the keys, it saves a significant amount of memory
        for word_id in list(inverted_barrel.keys()):
            this_entry = [word_id, fh.convert_to_csv(inverted_barrel[word_id])]
            inverted_barrel_entries.append(list(this_entry))
            offsets.append(offset)
            offset += get_byte_size(this_entry) + 1     # + 1 because length gives last byte of current line rather than first byte of next line
            del inverted_barrel[word_id]
            
        fh.write_to_csv(inverted_index_folder + f'/{barrel_number}.csv', inverted_barrel_entries, 'w')

        # calculate offsets for each line in csv and store them in a file
        packed_offsets = b''.join(struct.pack('I', offset) for offset in offsets)
        with open(inverted_index_folder + f'/{barrel_number}.bin', 'wb') as file:
            file.write(packed_offsets)
        
        barrel_number += 1
    else:
        print(f"Sorted {barrel_number} barrels.")
        break
