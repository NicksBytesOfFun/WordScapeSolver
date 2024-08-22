from itertools import permutations, chain, combinations


def readDictionary(trie):
    """
    Reads a dictionary of words from a file and populates a trie data structure.

    Args:
    - trie: The trie data structure to be populated.

    Returns:
    - The populated trie with the dictionary words.
    """
    # Select the appropriate file based on the mode
    file_name = "words"
    with open(file_name, "r") as my_file:
        print("Downloading Dictionary...")
        for word in my_file:
            word = word.strip().upper()
            if word == '0':  # Stop reading if '0' is encountered
                break
            trie.traverse_tree(word)
    print("Download Complete")
    return trie


def powerset(iterable):
    """
    Generates all possible subsets (the power set) of an iterable.

    Args:
    - iterable: The iterable to generate subsets from.

    Returns:
    - A generator for all subsets of the input iterable.
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def crackGame(tolerance, content_list):
    """
    Solves the Wordscapes game by finding all possible words that can be formed with the given letters.

    Args:
    - tolerance: Minimum number of characters a word must have to be considered.
    - content_list: The trie containing the dictionary words.

    Outputs:
    - Prints all possible word arrangements that meet the tolerance.
    """
    if tolerance <= 0:
        tolerance = 4

    letters = []
    output = []

    # Collect letters from the user until '0' is entered
    while True:
        letter = input("Letter: ").upper()
        if letter == '0':
            break
        letters.append(letter)

    # Generate all subsets of the collected letters and find permutations
    subsets = list(map(''.join, powerset(letters)))
    for subset in subsets:
        if len(subset) >= tolerance:
            perms = [''.join(p) for p in permutations(subset)]
            for word in perms:
                if word not in output and content_list.query(word):
                    output.append(word)

    # Clear screen and print results
    print("\n" * 20)
    print(f"Possible words with a minimum of {tolerance} characters include:")
    for word in output:
        print(word)
    print(f"Found {len(output)} possible word arrangements")


class SequenceDatabase:
    """
    A class representing a trie (prefix tree) data structure for storing sequences of characters.
    """

    def __init__(self):
        self.root = Node(None)

    def query(self, q):
        """
        Queries the trie for the existence of a given prefix.

        Args:
        - q: The prefix string to search for.

        Returns:
        - True if the prefix exists in the trie, False otherwise.
        """
        q += '['  # Append the end-of-word marker
        current_node = self.root

        for char in q:
            index = ord(char) - 65
            if not (0 <= index < 27) or current_node.children[index] == 0:
                return False
            current_node = current_node.children[index]

        return True

    def traverse_tree(self, s):
        """
        Adds a string to the trie. If the string already exists, increments its counter.

        Args:
        - s: The string to be added to the trie.
        """
        current_node = self.root

        for char in s:
            if char.isalpha():
                index = ord(char) - 65
                if current_node.children[index] != 0:  # Traverse existing node
                    current_node = current_node.children[index]
                else:  # Create a new node if necessary
                    new_node = Node(char)
                    current_node.children[index] = new_node
                    new_node.parent = current_node
                    new_node.depth = current_node.depth + 1
                    new_node.string = current_node.string + char
                    current_node = new_node

        # Mark the end of the word in the trie
        if current_node.children[-1] == 0:
            end_node = Node('[')
            current_node.children[-1] = end_node
            end_node.parent = current_node
            end_node.string = current_node.string
            end_node.max_string = current_node.string
            end_node.depth = current_node.depth + 1
            current_node.children_number += 1
        else:
            current_node.children[-1].traversal_counter += 1

    def addSequence(self, s):
        """
        Wrapper function to add a sequence to the trie.

        Args:
        - s: The sequence to be added.
        """
        self.traverse_tree(s)


class Node:
    """
    A class representing a node in the trie.
    """

    def __init__(self, item=None):
        self.item = item
        self.children = [0] * 27  # 26 letters + 1 for end-of-word marker '['
        self.children_number = 0
        self.traversal_counter = 1
        self.parent = None
        self.string = ''
        self.max_node = None
        self.max_string = ''
        self.depth = 0


if __name__ == '__main__':
    sq = SequenceDatabase()
    readDictionary(sq, 0)
    choice = input("Choose 1 to continue or 0 to end: ")
    while choice == '1':
        crackGame(4, sq)
        choice = input("Choose 1 to continue or 0 to end: ")
