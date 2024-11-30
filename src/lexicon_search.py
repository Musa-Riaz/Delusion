import json
import hashlib

# Function to generate word IDs using hashing
def generate_word_id(word):
    return int(hashlib.sha256(word.encode()).hexdigest(), 16) % (10**8)




# Function to search for a word in the lexicon
def search_word(word):
    #loading the lexicon
    with open('lexicon.json', 'r', encoding='utf-8') as file:
        lexicon = json.load(file)
    word_id = generate_word_id(word)  # Generate the word ID
    if str(word_id) in lexicon:       # Check if word ID exists in lexicon
        print(f"The word '{word}' exists in the lexicon with ID: {word_id}")
        return lexicon[str(word_id)]
    else:
        print(f"The word '{word}' does not exist in the lexicon.")
        return None

search_word('military')  