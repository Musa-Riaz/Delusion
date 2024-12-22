from sortedcontainers import SortedList

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Trie:
    def __init__(self, num_results):
        self.root = TrieNode()
        self.num_results = num_results
          
    def insert(self, word, frequency):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # store word if it is more frequent than the existing n words
        # or there are less than n words
        node.word = (-1 * frequency, word)

    def autocomplete(self, prefix):
        node = self.root
        # traverse the trie with the prefix chars
        for char in prefix:
            if char not in node.children:
                return []   # no words exist with the prefix
            node = node.children[char]
      
        # collect the top n words from this prefix
        result = SortedList()
        self._collect_words(node, result)
        result = [word[1] for word in result]
        return result
    
    def _collect_words(self, node, result):
        # stores a list of 8 words sorted on frequency
        if node.word:
            if len(result) < self.num_results:
                result.add(node.word)
            elif node.word[0] < result[-1][0]:
                result.pop()
                result.add(node.word)

        # recursively collect each child's words if it has a higher frequency
        for child in node.children.values():
            self._collect_words(child, result)
