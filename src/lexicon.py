import pandas as pd
import re
import nltk
import json
import os
from nltk.corpus import stopwords
import hashlib
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Loading the CSV file, im using the practice_dataset which I made for testing. Also I have used the title column for processing the text
data_file = pd.read_csv('practice_dataset.csv')

# Replacing missing values with an empty string so that it may not cause any problem during processing
data_file['title'] = data_file['title'].fillna('')

# setting common english words as stop words
stop_words = set(stopwords.words('english'))

# Define the preprocessing function
def preprocess_text(text):
    text = text.lower()  # Converting the text to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters and punctuation using regular expressions
    word_tokens = word_tokenize(text)  # Tokenize the cleaned text into individual words.
    filtered_tokens = [word for word in word_tokens if word not in stop_words]  # Remove stop words to keep only important words.
    return filtered_tokens

# Apply preprocessing to the 'text' column
data_file['processed_text'] = data_file['text'].apply(preprocess_text)


def generate_word_id(word):
    return int(hashlib.sha256(word.encode()).hexdigest(), 16) % (10**8)

lexicon ={} #storing as dictionary
for index, row in data_file.iterrows():
    text = row['text']  # Adjust the column name based on your dataset
    words = text.lower().split()  # Simple tokenization (better to use nltk's tokenizer)


for word in words:
    # Check if the word is already in the lexicon
        if word not in lexicon:
            word_id = generate_word_id(word)  # Generate and store the word ID
            lexicon[word] = word_id
   

# Save lexicon to file
with open('lexicon.json', 'w', encoding='utf-8') as file:
    json.dump(lexicon, file, indent=4)


print("lexicon.json file created successfully")


