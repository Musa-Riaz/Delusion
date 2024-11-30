import pandas as pd
import re
import nltk
import json
import hashlib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

with open('lexicon.json', 'r', encoding = 'utf-8') as file:
    lexicon = json.load(file)

data_file = pd.read_csv('practice_dataset.csv')
data_file['title'] = data_file['title'].fillna('')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    word_tokens = word_tokenize(text)
    return [word for word in word_tokens if word not in stop_words]

# Applying preprocessing to the dataset
data_file['processed_text'] = data_file['title'].apply(preprocess_text)

print(data_file)

# Initialize the forward index
forward_index = {}

# Populate the forward index
for doc_id, row in data_file.iterrows():
    text = row['text']
    words = preprocess_text(text)  # Preprocess text for the document
    word_positions = {}  # Store word positions for this document

    # Iterate through words and record positions
    for position, word in enumerate(words):
        word_id = lexicon.get(word)
        if word_id:  # If the word exists in the lexicon
            if word_id not in word_positions:
                word_positions[word_id] = []
            word_positions[word_id].append(position)

    # Store the word positions in the forward index (docId -> wordId -> positions)
    forward_index[doc_id] = word_positions

# Save the forward index to a JSON file
with open('forward_index.json', 'w', encoding='utf-8') as file:
    json.dump(forward_index, file, indent=4)

print("Forward index file created successfully")