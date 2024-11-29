# this is the sorter of the search engine, converting forward index into inverted index
# initial version, assumes no barrels are implemented, not intended to function efficiently for the entire forward index without barrel divisions
import json

with open('forward.json', 'r') as data:
    forward = json.load(data)

inverted = {}

for docID in forward:
    # thisIndex is all the words in the current document with their hitlists
    thisIndex = forward[docID]
    for wordID in thisIndex:
        if wordID not in inverted:
            # initialize a dict for this wordID
            inverted[wordID] = {}
        # append this docID : hitlist to this word's entry
        inverted[wordID][docID] = thisIndex[wordID]

with open('inverted.json', 'w') as output:
    json.dump(inverted, output)
