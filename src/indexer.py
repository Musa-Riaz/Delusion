import word_processing as wp
import csv
import json
import regex as re

# hits are represented as 2 integers
# the first integer represents the nature of the hit
# 0 : title, 1 : text, 2 : URL, 3 : authors, 5 : tags
# the remaining represents the position of the hit
# positions > 9999 are stored as 9999

dataset_file = 'src/practice_dataset.csv'
lexicon_file = 'src/lexicon.json'
ids_file = 'src/next_word_id.txt'

try:
    with open(ids_file, 'r') as file:
        next_word_id = int(file.readline())
        next_doc_id = int(file.readline())
except:
    next_word_id = 0
    next_doc_id = 0

try:
    file = open(dataset_file, encoding='utf-8')
except IOError:
    print(f"Couldn't open {dataset_file}")

new_words = {}
try:
    with open(lexicon_file) as file:
        lexicon = json.load(file)
except IOError:
    lexicon = {}

TITLE = 0
TEXT = 1
URL = 2
AUTHORS = 3
TAGS = 5

reader = csv.reader(file)
next(reader)    # skip headings row
forward_index = {}  # TODO: optimize to write entries to file in chunks
for row in reader:
    this_entry = {}
    for column in [TITLE, TEXT, URL, AUTHORS, TAGS]:
        pos = 0

        if column == TITLE or column == TEXT:
            tagged_text = wp.tag_text(row[column])
        elif column == AUTHORS or column == TAGS:
            tagged_text = wp.tag_text(' '.join(row[column]))
        else:
            # extracting relevant text from URL using regex
            match = re.search(r"medium\.com\/(.+)-(.+)$", row[column])  # get remaining text after 'medium.com'
            tagged_text = wp.tag_text(' '.join(re.split(r'[/-]', match.group(1))))  # split the text on / or - and join with spaces

        for word, tag in tagged_text:
            this_word = wp.process_word(word, tag)
            if this_word == '':
                continue
            if this_word not in lexicon:
                this_word_id = next_word_id
                lexicon[this_word] = this_word_id
                new_words[this_word] = this_word_id
                new_words[this_word] = this_word_id
                next_word_id += 1
            else:
                this_word_id = lexicon[this_word]

            if this_word_id not in this_entry:
                this_entry[this_word_id] = []

            this_hit = column * 10000 + pos
            this_entry[this_word_id].append(this_hit)
            pos += 1
        
    forward_index[next_doc_id] = this_entry
    next_doc_id += 1
        
print(json.dumps(forward_index, indent=4))

file.close()
