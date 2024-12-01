# contains word processing functions
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import string
import regex as re

lemmatizer = WordNetLemmatizer()
# set of common words not considered by the search engine
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    print("Missing nltk resources, consider running nltk_download.py")

# tags words in text based off part-of-speech
def tag_text(text):
    text = text.lower()
    text = text.encode('ascii', 'ignore').decode('ascii')   # removing non-ascii characters
    try:
        tokens = word_tokenize(text)
        # add words to a list
        # remove punctuation
        # split words on / and - to avoid cases like brain/mental being 1 word
        processed_tokens = []
        for word in tokens:
            if word not in string.punctuation:
                for split_word in re.split(r'[/-]', word):
                    processed_tokens.append(split_word)
        return pos_tag(processed_tokens)
    except LookupError:
        print("Missing nltk resources, consider running nltk_download.py")

def process_word(word, tag):
    # return an empty string if the word is a stop word or a letter
    if word in stop_words or len(word) == 1:
        return ''
    
    # lemmatizing based off of tag
    if tag.startswith('NN'):
        processed = lemmatizer.lemmatize(word, pos='n')  # noun
    elif tag.startswith('VB'):
        processed = lemmatizer.lemmatize(word, pos='v')  # verb
    elif tag.startswith('JJ'):
        processed = lemmatizer.lemmatize(word, pos='a')  # adjective
    else:
        processed = lemmatizer.lemmatize(word)
    
    # to prevent some unexpected results such as 'better' -> 'b'
    if len(processed) <= 1:
        return word
    
    return processed
