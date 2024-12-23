from file_handling import load_frequencies
from sortedcontainers import SortedList
from random import choice
import file_handling

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
          
    def insert(self, word, frequency):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # store word if it is more frequent than the existing n words
        # or there are less than n words
        node.word = (-1 * frequency, word)

    def autocomplete(self, prefix, num_results):
        node = self.root
        # traverse the trie with the prefix chars
        for char in prefix:
            if char not in node.children:
                return []   # no words exist with the prefix
            node = node.children[char]
      
        # collect the top n words from this prefix
        result = SortedList()
        self._collect_words(node, result, num_results)
        result = [word[1] for word in result]
        return result
    
    def _collect_words(self, node, result, num_results):
        # stores a list of 8 words sorted on frequency
        if node.word:
            if len(result) < num_results:
                result.add(node.word)
            elif node.word[0] < result[-1][0]:
                result.pop()
                result.add(node.word)

        # recursively collect each child's words if it has a higher frequency
        for child in node.children.values():
            self._collect_words(child, result, num_results)


def create_autocomplete_trie(num_words, lexicon):
    trie = Trie()
    frequencies = load_frequencies('indexes/frequencies.bin')
    for word in lexicon:
        word_id = lexicon[word]
        if word_id > num_words:
            break
        trie.insert(word, frequencies[word_id])
    return trie

def get_suggestions(trie, lexicon, prefix, num_results):
    if prefix == '':
        return [choice(lexicon.keys()) for i in range(num_results)]
    return trie.autocomplete(prefix, num_results)
