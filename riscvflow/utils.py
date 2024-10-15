
numLines = 0


def get_zeros(num):
    # with max length from numLines, convert num to string with prefix 0s
    return f'{num:0{len(str(numLines))}d}'


def set_numLines(num):
    global numLines
    numLines = num


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end


def build_trie(words):
    root = TrieNode()
    for word in words:
        root.insert(word)
    return root

