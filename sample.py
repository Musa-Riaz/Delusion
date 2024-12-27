import re
def process_words_in_text(text):
    return re.findall(r'\b\w+\b', text.lower())
def find_sentence_with_word(text, word):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    for sentence in sentences:
        if word.lower() in process_words_in_text(sentence):
            return sentence
    return None
def extract_window_from_sentence(sentence, word, max_words):
    words = process_words_in_text(sentence)
    word_index = words.index(word.lower()) if word.lower() in words else -1
    if word_index == -1:
        return None
    if word_index < max_words:
        return " ".join(words[:max_words])
    start_index = word_index
    return " ".join(words[start_index:start_index + max_words])
def search_hits_in_text(text, search_word, max_words):
    search_word = search_word.lower()
    sentence = find_sentence_with_word(text, search_word)
    if sentence:
        window = extract_window_from_sentence(sentence, search_word, max_words)
        return {
            'word': search_word,
            'sentence': sentence,
            'window': window
        }
    return {
        'word': None,
        'sentence': None,
        'window': f"The word '{search_word}' was not found in the text."
    }
def main(text, search_word, max_words):
    result = search_hits_in_text(text, search_word, max_words)
    total_words = len(process_words_in_text(text))
    print(f"Total words in text: {total_words}")
    print(f"Requested words to display: {max_words}")
    if result['word']:
        print(f"Word: {result['word']}")
        print(f"Sentence: {result['sentence']}")
        print(f"Window with {max_words} words: {result['window']}")
    else:
        print("The word wasn't found in the text.")
        print(f"Fallback: {result['window']}")
text = (
    "Although the sky was overcast and the wind howled ominously through the dense forest, a group of determined hikers, equipped with sturdy boots, heavy backpacks, and an unshakable sense of adventure, pressed forward along the winding trail, marveling at the towering trees, hidden wildlife, and the faint promise of sunlight breaking through the clouds."
)
search_word = "marveling"
max_words = 30
main(text, search_word, max_words)












