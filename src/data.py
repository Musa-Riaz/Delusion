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
data_file = pd.read_csv(r'C:\Users\Home PC\OneDrive\Desktop\DSA_Project\Delusion\src\practice_dataset.csv')

# Replacing missing values with an empty string so that it may not cause any problem during processing
data_file['text'] = data_file['text'].fillna('')

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
data_file['processed_text'] = data_file['title'].apply(preprocess_text)

# Display the processed text
print(data_file['processed_text'].head())

def generate_word_id(word):
    return int(hashlib.sha256(word.encode()).hexdigest(), 16) % (10**8)

lexicon ={} #storing as dictionary
for index, row in data_file.iterrows():
    tokens = set(row['processed_text'])
    for word in tokens:
        word_id = generate_word_id(word) #generating a unique id for each word
        if word_id not in lexicon:
            lexicon[word_id] = word


# Save lexicon to file
with open('lexicon.json', 'w', encoding='utf-8') as file:
    json.dump(lexicon, file, indent=4)


# # Build the lexicon
# lexicon = {}
# for index, row in data_file.iterrows():
#     tokens = row['processed_text']
#     for position, word in enumerate(tokens):
#         if word not in lexicon:
#             lexicon[word] = {}
#         if index not in lexicon[word]:
#             lexicon[word][index] = []
#         lexicon[word][index].append(position)

# #creating a folder to store files
# output_folder = "processed_text_files"
# os.makedirs(output_folder, exist_ok=True)

# # Save each processed row into its own file
# for index, row in data_file.iterrows():
#     filename = os.path.join(output_folder, f"article_{index}.txt")
#     with open(filename, 'w', encoding='utf-8') as file:
#         file.write(" ".join(row['processed_text']))  # Join tokens back into a single string

# # Split the lexicon into multiple parts (for example, each part has 100 words)
# chunk_size = 100
# lexicon_items = list(lexicon.items())

# # Create a folder to store lexicon chunks
# lexicon_folder = "lexicon_files"
# os.makedirs(lexicon_folder, exist_ok=True)

# # Save each chunk to a separate file
# for i in range(0, len(lexicon_items), chunk_size):
#     chunk = dict(lexicon_items[i:i + chunk_size])
#     filename = os.path.join(lexicon_folder, f"lexicon_part_{i // chunk_size + 1}.txt")
#     with open(filename, 'w', encoding='utf-8') as file:
#         file.write(json.dumps(chunk, indent=4))  # Save the chunk as formatted JSON in txt

# # Check a few files from the output folders
# print("Sample processed text file:")
# with open(os.path.join(output_folder, 'article_0.txt'), 'r', encoding='utf-8') as file:
#     print(file.read())

# print("\nSample lexicon chunk file:")
# with open(os.path.join(lexicon_folder, 'lexicon_part_1.txt'), 'r', encoding='utf-8') as file:
#     print(file.read())

# # Save the DataFrame with processed text to a CSV file
# data_file.to_csv('processed_medium_articles.csv', index=False)

# # Save the lexicon to a JSON file (suitable for nested data)
# with open('lexicon.json', 'w') as json_file:
#     json.dump(lexicon, json_file, indent=4)

# # Load and verify the saved lexicon
# with open('lexicon.json', 'r') as json_file:
#     loaded_lexicon = json.load(json_file)
# print(list(loaded_lexicon.items())[:5])  # Print first 5 items for verification
