import file_handling as fh
import file_paths as fp
import struct
import json
import ast
import os

BARREL_SIZE = 1000

def get_byte_size(entry):
    entry[1] = '"' + str(entry[1]) + '"'
    csv_line = ','.join(map(str, entry)) + '\n'
    return len(csv_line)

def sort_barrel(forward_barrel):
    frequencies = [0 for i in range(BARREL_SIZE)]      # for storing frequencies of words for auto-complete
    inverted_barrel = {}
    max_word_id = 0
    
    for doc_id in list(forward_barrel.keys()):
            # this_index is all the words in the current document with their hitlists
            this_index = forward_barrel[doc_id]
            
            # free memory of this forward entry
            del forward_barrel[doc_id]

            for word_id in this_index:
                hit_list = this_index[word_id]
                if word_id not in inverted_barrel:
                    # initialize a dict for this word_id
                    inverted_barrel[word_id] = {}

                # append this {doc_id : hitlist} to this word's entry and sum its frequency
                inverted_barrel[word_id][doc_id] = hit_list
                frequencies[word_id % BARREL_SIZE] += len(hit_list)
                max_word_id = max(max_word_id, word_id % BARREL_SIZE)
    
    if max_word_id != 999:
        frequencies = frequencies[:max_word_id + 1]
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
        del inverted_barrel[word_id]    # freeing memory from the dictionary
    
    return inverted_barrel_entries, offsets, frequencies

def sort_all_barrels():
    os.makedirs('indexes/inverted_index', exist_ok=True)
    open(fp.frequencies_file, 'w')     # rewrite file

    barrel_number = 0
    while True:
        barrel_path = fp.forward_index_folder + f'/{barrel_number}.csv'
        if os.path.isfile(barrel_path):
            forward_barrel = fh.load_forward_barrel(barrel_path)
                        
            print(f"Sorting barrel {barrel_number}...")
            inverted_barrel_entries, offsets, frequencies = sort_barrel(forward_barrel)
                
            fh.write_to_csv(fp.inverted_index_folder + f'/{barrel_number}.csv', inverted_barrel_entries, 'w')
    
            # calculate offsets for each line in csv and store them in a file
            packed_offsets = b''.join(struct.pack('I', offset) for offset in offsets)
            with open(fp.inverted_index_folder + f'/{barrel_number}.bin', 'wb') as file:
                file.write(packed_offsets)
            
            packed_frequencies = b''.join(struct.pack('I', frequency) for frequency in frequencies)
            with open(fp.frequencies_file, 'ab') as file:
                file.write(packed_frequencies)
            
            barrel_number += 1
        else:
            print(f"Sorted {barrel_number} barrels.")
            break
        
# adds a single forward index entry to a barrel
# inverted barrel is read line by line in binary and copied to a temp file
# modified lines are modified and rewritten
def add_to_inv_barrel(entry, barrel_num):
    # hitlist is empty
    if len(entry[1]) == 0:
        return
    
    print(f"Adding entry {entry} to inverted barrel {barrel_num}...")
    barrel_path = fp.inverted_index_folder + f'/{barrel_num}'
    if not os.path.exists(barrel_path + '.csv'):
        # create empty barrel if it doesnt exist
        with open(barrel_path + '.csv', 'w'):
            pass
        
    offsets = []
    current_offset = 0
    with open(barrel_path + '.csv', 'rb') as barrel, open(barrel_path + 't.csv', 'wb') as temp_barrel, open(barrel_path + '.bin', 'wb') as offsets_file:
        current_word = 0
        current_line = 0
        word_line = entry[1][current_word][0] % BARREL_SIZE     # word_id % barrel_size
        for line in barrel:
            if current_line == word_line:
                line = line.decode()
                line = list(ast.literal_eval(line))
                line[1] = json.loads(line[1])
                line[1].append([entry[0], entry[1][current_word][1]])
                line = str(line[0]) + ',"' + str(line[1]) + '"\n'
                line = line.encode()
                current_word += 1
                if current_word < len(entry[1]):
                    word_line = entry[1][current_word][0] % BARREL_SIZE
            
            temp_barrel.write(line)
            offsets.append(current_offset)
            current_offset += len(line)
            current_line += 1
    
        for word in entry[1][current_word:]:
            line = str(word[0]) + ',"' + str([[entry[0], word[1]]]) + '"\n'
            line = line.encode()
            temp_barrel.write(line)
            offsets.append(current_offset)
            current_offset += len(line)
        
        packed_offsets = b''.join(struct.pack('I', offset) for offset in offsets)
        offsets_file.write(packed_offsets)
    
    os.replace(barrel_path + 't.csv', barrel_path + '.csv')

# sort_all_barrels()
